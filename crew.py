"""
crew.py
--------
Wires agents and tasks into a single sequential Crew and exposes one
public function, run_career_crew(), which app.py calls.

Keeping this orchestration logic separate from app.py means the same
crew can be reused from a CLI script, a test, or a different UI later.
"""

from pathlib import Path

from crewai import Crew, Process

from agents import build_all_agents
from tasks import build_all_tasks
from tools import extract_resume_text
from config import settings

# Cap how much raw resume text gets injected into the first task's prompt.
# Very long resumes (multi-page, dense) can otherwise push a single request
# over an account's tokens-per-minute limit. ~6000 characters is generous
# for a 1-3 page resume while keeping prompts well within typical rate caps.
MAX_RESUME_PREVIEW_CHARS = 6000


def run_career_crew(resume_pdf_path: str) -> str:
    """
    Execute the full career-analysis pipeline for one resume.

    Args:
        resume_pdf_path: Absolute path to the uploaded resume PDF.

    Returns:
        The full Markdown text of the generated career report.

    Raises:
        FileNotFoundError, ValueError: propagated from PDF extraction if the
            file is missing or unreadable.
        RuntimeError: if the crew runs but produces no output file.
    """
    settings.validate()

    resume_text_preview = extract_resume_text(resume_pdf_path)
    if len(resume_text_preview) > MAX_RESUME_PREVIEW_CHARS:
        resume_text_preview = (
            resume_text_preview[:MAX_RESUME_PREVIEW_CHARS]
            + "\n\n[...resume truncated for length; full text remains searchable via the PDF tool...]"
        )

    agents = build_all_agents(resume_pdf_path)
    report_output_path = str(settings.REPORTS_DIR / settings.REPORT_FILENAME)
    tasks = build_all_tasks(agents, resume_text_preview, report_output_path)

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        # Throttles total requests per minute across all agents so a burst
        # of back-to-back calls doesn't blow past an account's rate limit.
        # Lower this further (e.g. 2) if you're still hitting 429 errors.
        max_rpm=5,
    )

    crew.kickoff()

    output_path = Path(report_output_path)
    if not output_path.exists():
        raise RuntimeError(
            "Crew finished but no report file was produced. Check agent logs."
        )

    return output_path.read_text(encoding="utf-8")
