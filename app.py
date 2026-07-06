"""
app.py
-------
Streamlit front-end for the Career AI Assistant.

Flow:
1. User uploads a resume PDF.
2. User clicks "Analyze".
3. A progress bar reflects the pipeline stages while the CrewAI crew runs.
4. Results (resume summary, skill charts, jobs, interview questions,
   roadmap) are displayed, and the full report is downloadable.
"""

import re
import uuid
from pathlib import Path

import streamlit as st

from config import settings
from crew import run_career_crew

# --- Page setup ---
st.set_page_config(page_title="AI Career Assistant", page_icon="🧭", layout="wide")
st.title("🧭 Agentic AI Career Assistant")
st.caption(
    "Upload your resume and get an AI-generated skill analysis, job matches, "
    "interview questions, and a personalized learning roadmap."
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

    Args:
        report_md: Full Markdown text of the report.

    Returns:
        Dict mapping section title -> section body text.
    """
    sections = {}
    parts = re.split(r"^##\s+(.*)$", report_md, flags=re.MULTILINE)
    # parts[0] is any preamble before the first heading; skip it if empty.
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        sections[title] = body
    return sections


def save_uploaded_pdf(uploaded_file) -> str:
    """
    Persist an uploaded Streamlit file to disk inside this project's own
    data/ directory (rather than the OS temp folder), since PDFSearchTool's
    path-safety check only permits reading files from within an allowed
    directory tree.

    Each upload gets a unique filename so concurrent sessions never collide.

    Args:
        uploaded_file: The Streamlit UploadedFile object.

    Returns:
        Absolute path to the saved PDF file.
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
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    if size_mb > settings.MAX_RESUME_FILE_MB:
        st.error(
            f"File is {size_mb:.1f} MB, which exceeds the "
            f"{settings.MAX_RESUME_FILE_MB} MB limit."
        )
    elif st.button("Analyze", type="primary"):
        progress_bar = st.progress(0, text=PIPELINE_STAGES[0])
        try:
            resume_path = save_uploaded_pdf(uploaded_file)

            # The crew runs as one blocking call under the hood. We can't get
            # true per-agent progress callbacks without deeper CrewAI hooks,
            # so we animate the bar through the known stages to keep the
            # user informed while `run_career_crew` executes.
            for i, stage in enumerate(PIPELINE_STAGES[:-1]):
                progress_bar.progress(
                    int((i / len(PIPELINE_STAGES)) * 100), text=stage
                )

            report_md = run_career_crew(resume_path)

            progress_bar.progress(100, text=PIPELINE_STAGES[-1])
            st.session_state["report_md"] = report_md
            st.success("Analysis complete!")

        except (FileNotFoundError, ValueError) as exc:
            st.error(f"Could not read resume: {exc}")
        except EnvironmentError as exc:
            st.error(f"Configuration error: {exc}")
        except Exception as exc:  # noqa: BLE001 - surface any crew failure to the user
            st.error(f"Something went wrong while analyzing your resume: {exc}")

# --- Results display ---
if "report_md" in st.session_state:
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
