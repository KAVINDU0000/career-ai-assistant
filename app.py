"""
app.py
-------
Streamlit front-end for the Career AI Assistant.

Flow:
1. User logs in or signs up (auth_ui.render_auth_gate).
2. User uploads a resume PDF.
3. User clicks "Analyze".
4. A progress bar reflects the pipeline stages while the CrewAI crew runs.
5. Results are displayed in tabs, saved to the user's history, and the
   full report is downloadable.
"""

import re
import uuid

import streamlit as st

from config import settings
from crew import run_career_crew
from auth_ui import render_auth_gate, render_user_badge_and_logout
from styles import inject_custom_css, render_hero, render_theme_toggle

# --- Page setup ---
st.set_page_config(page_title="AI Career Assistant", page_icon="🧭", layout="wide")
render_theme_toggle()
inject_custom_css()

# --- Auth gate: stop here if not logged in ---
if not render_auth_gate():
    st.stop()

render_user_badge_and_logout()

render_hero(
    title="🧭 Agentic AI Career Assistant",
    subtitle="Upload your resume and get an AI-generated skill analysis, job matches, "
             "interview questions, and a personalized learning roadmap.",
    badge="MULTI-AGENT AI",
)

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


# --- Sidebar: config sanity check ---
with st.sidebar:
    st.header("Setup status")
    if settings.OPENAI_API_KEY:
        st.success("OPENAI_API_KEY loaded")
    else:
        st.error("OPENAI_API_KEY missing - add it to your .env file")
    st.write(f"Model: `{settings.OPENAI_MODEL_NAME}`")

# --- Upload + analyze ---
st.subheader("📄 Upload your resume")
uploaded_file = st.file_uploader("PDF only", type=["pdf"], label_visibility="collapsed")

if uploaded_file is not None:
    size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    if size_mb > settings.MAX_RESUME_FILE_MB:
        st.error(
            f"File is {size_mb:.1f} MB, which exceeds the "
            f"{settings.MAX_RESUME_FILE_MB} MB limit."
        )
    elif st.button("✨ Analyze", type="primary"):
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

        except (FileNotFoundError, ValueError) as exc:
            st.error(f"Could not read resume: {exc}")
        except EnvironmentError as exc:
            st.error(f"Configuration error: {exc}")
        except Exception as exc:  # noqa: BLE001
            st.error(f"Something went wrong while analyzing your resume: {exc}")

# --- Results display ---
if "report_md" in st.session_state:
    st.divider()
    report_md = st.session_state["report_md"]
    sections = split_report_sections(report_md)

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
    )
