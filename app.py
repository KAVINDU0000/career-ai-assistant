"""
app.py
-------
Streamlit front-end for the Career AI Assistant.

Flow:
1. User logs in or signs up (auth_ui.render_auth_gate).
2. User sees a personalized welcome strip and an icon-header upload card.
3. User clicks "Analyze".
4. A progress bar reflects the pipeline stages while the CrewAI crew runs.
5. Results are displayed with a real data stats strip, tabs inside a card,
   saved to the user's history, and the full report is downloadable.
"""

import re
import uuid

import streamlit as st

from config import settings
from crew import run_career_crew
from auth_ui import render_auth_gate, render_user_badge_and_logout
from database.db import init_db
from database.crud import get_all_reports
from styles import inject_custom_css, render_brand_bar, render_section_label, _clean

# --- Page setup ---
st.set_page_config(page_title="AI Career Assistant", page_icon="🧭", layout="wide")
inject_custom_css()

# --- Auth gate: stop here if not logged in ---
if not render_auth_gate():
    st.stop()

render_user_badge_and_logout()
render_brand_bar()

PIPELINE_STAGES = [
    "Reading resume",
    "Analyzing skills",
    "Matching jobs",
    "Preparing interview questions",
    "Building learning roadmap",
    "Writing final report",
]


def split_report_sections(report_md: str) -> dict:
    """
    Split the combined career_report.md into its top-level (##) sections
    so the UI can render each one in its own tab instead of one giant blob.
    """
    sections = {}
    parts = re.split(r"^##\s+(.*)$", report_md, flags=re.MULTILINE)
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        sections[title] = body
    return sections


def extract_overall_score(report_md: str) -> str:
    """Best-effort extraction of the numeric score for display in the stats strip."""
    match = re.search(r"(\d{1,3})\s*/\s*100", report_md)
    return f"{match.group(1)}/100" if match else "N/A"


def count_recommended_jobs(sections: dict) -> str:
    """Rough count of recommended jobs by counting table/list rows in that section."""
    jobs_text = sections.get("Recommended Jobs", "")
    rows = [line for line in jobs_text.splitlines() if line.strip().startswith("|") and "---" not in line]
    count = max(len(rows) - 1, 0) if rows else 0
    return str(count) if count > 0 else "-"


def save_uploaded_pdf(uploaded_file) -> str:
    """
    Persist an uploaded Streamlit file to disk inside this project's own
    data/ directory, since PDFSearchTool's path-safety check only permits
    reading files from within an allowed directory tree.
    """
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    unique_name = f"resume_{uuid.uuid4().hex}.pdf"
    dest_path = settings.DATA_DIR / unique_name
    dest_path.write_bytes(uploaded_file.getvalue())
    return str(dest_path)


# --- Personalized welcome strip ---
init_db()
user_email = st.session_state["user"]["email"]
report_count = len(get_all_reports(st.session_state["user"]["id"]))

st.markdown(
    _clean(f"""
    <div class="hero-section" style="padding-top:0.4rem;">
        <div class="hero-badge">👋 WELCOME BACK</div>
        <div class="hero-title" style="font-size:2rem;">{user_email.split('@')[0].title()}, ready for your next move?</div>
        <div class="hero-subtitle" style="max-width:600px;">
            {"You have " + str(report_count) + " saved report(s) - " if report_count else "You haven't analyzed a resume yet - "}
            upload a new one below to get a fresh skill analysis, job matches, and roadmap.
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)

# --- Sidebar: config sanity check ---
with st.sidebar:
    st.header("Setup status")
    if settings.OPENAI_API_KEY:
        st.success("OPENAI_API_KEY loaded")
    else:
        st.error("OPENAI_API_KEY missing - add it to your .env file")
    st.write(f"Model: `{settings.OPENAI_MODEL_NAME}`")

# --- Upload card, with an icon-circle header matching the landing page's feature cards ---
render_section_label("STEP 1 · GET STARTED")

with st.container(border=True):
    st.markdown(
        _clean("""
        <div style="display:flex; align-items:center; gap:0.9rem; margin-bottom:1rem;">
            <div class="feature-icon-circle" style="margin:0;">📄</div>
            <div>
                <div class="feature-title" style="margin-bottom:0.1rem;">Upload your resume</div>
                <div class="feature-desc">PDF only, up to 10 MB. We'll extract the text automatically.</div>
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("PDF only, up to 10 MB", type=["pdf"], label_visibility="collapsed")

    if uploaded_file is not None:
        size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        if size_mb > settings.MAX_RESUME_FILE_MB:
            st.error(
                f"File is {size_mb:.1f} MB, which exceeds the "
                f"{settings.MAX_RESUME_FILE_MB} MB limit."
            )
        elif st.button("✨ Analyze My Resume", type="primary", use_container_width=True):
            progress_bar = st.progress(0, text=PIPELINE_STAGES[0])
            try:
                resume_path = save_uploaded_pdf(uploaded_file)
                user_id = st.session_state["user"]["id"]

                for i, stage in enumerate(PIPELINE_STAGES[:-1]):
                    progress_bar.progress(
                        int((i / len(PIPELINE_STAGES)) * 100), text=stage
                    )

                result = run_career_crew(
                    resume_path,
                    user_id=user_id,
                    original_filename=uploaded_file.name,
                )
                report_md = result["report_markdown"]

                progress_bar.progress(100, text=PIPELINE_STAGES[-1])
                st.session_state["report_md"] = report_md
                st.success("Analysis complete! Saved to your report history.")
                st.rerun()

            except (FileNotFoundError, ValueError) as exc:
                st.error(f"Could not read resume: {exc}")
            except EnvironmentError as exc:
                st.error(f"Configuration error: {exc}")
            except Exception as exc:  # noqa: BLE001
                st.error(f"Something went wrong while analyzing your resume: {exc}")

# --- Results display ---
if "report_md" in st.session_state:
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_label("STEP 2 · YOUR RESULTS")

    report_md = st.session_state["report_md"]
    sections = split_report_sections(report_md)

    st.markdown(
        _clean(f"""
        <div class="stats-bar">
            <div class="stat-item"><div class="stat-number">{extract_overall_score(report_md)}</div><div class="stat-label">Overall Score</div></div>
            <div class="stat-item"><div class="stat-number">{count_recommended_jobs(sections)}</div><div class="stat-label">Jobs Matched</div></div>
            <div class="stat-item"><div class="stat-number">6</div><div class="stat-label">AI Agents Used</div></div>
            <div class="stat-item"><div class="stat-number">✓</div><div class="stat-label">Saved to History</div></div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        tab_names = [
            "Resume Summary",
            "Skill Analysis",
            "Recommended Jobs",
            "Interview Questions",
            "Learning Roadmap",
            "Career Advice",
            "Overall Resume Score",
        ]
        available_tabs = [name for name in tab_names if name in sections]
        tabs = st.tabs(available_tabs if available_tabs else ["Full Report"])

        if available_tabs:
            for tab, name in zip(tabs, available_tabs):
                with tab:
                    st.markdown(sections[name])
        else:
            with tabs[0]:
                st.markdown(report_md)

        st.divider()
        st.download_button(
            label="📥 Download Full Report (Markdown)",
            data=report_md,
            file_name=settings.REPORT_FILENAME,
            mime="text/markdown",
            use_container_width=True,
        )
