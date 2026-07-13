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
from database.db import init_db
from database.crud import save_resume, save_report

# Cap how much raw resume text gets injected into the first task's prompt.
# Very long resumes (multi-page, dense) can otherwise push a single request
# over an account's tokens-per-minute limit. ~6000 characters is generous
# for a 1-3 page resume while keeping prompts well within typical rate caps.
MAX_RESUME_PREVIEW_CHARS = 6000


def run_career_crew(resume_pdf_path: str, user_id: int, original_filename: str = None) -> dict:
    """
    Execute the full career-analysis pipeline for one resume, and persist
    both the resume and the generated report to the database under the
    given user's account.

    Args:
        resume_pdf_path: Absolute path to the uploaded resume PDF.
        user_id: id of the logged-in user this resume belongs to.
        original_filename: The user's original filename, for display in the
            History page. Falls back to the path's basename if not given.

    Returns:
        A dict: {"report_markdown": str, "resume_id": int, "report_id": int}

    Raises:
        FileNotFoundError, ValueError: propagated from PDF extraction if the
            file is missing or unreadable.
        RuntimeError: if the crew runs but produces no output file.
    """
    settings.validate()
    init_db()

    resume_text_full = extract_resume_text(resume_pdf_path)
    resume_text_preview = resume_text_full
    if len(resume_text_preview) > MAX_RESUME_PREVIEW_CHARS:
        resume_text_preview = (
            resume_text_preview[:MAX_RESUME_PREVIEW_CHARS]
            + "\n\n[...resume truncated for length; full text remains searchable via the PDF tool...]"
        )

    filename = original_filename or Path(resume_pdf_path).name
    resume_id = save_resume(user_id=user_id, filename=filename, raw_text=resume_text_full)

    agents = build_all_agents()
    report_output_path = str(settings.REPORTS_DIR / settings.REPORT_FILENAME)
    tasks = build_all_tasks(agents, resume_text_preview, report_output_path)
    resume_task, skill_task, job_task, interview_task, roadmap_task, report_task = tasks

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

    # Assemble the final report programmatically from each task's own
    # output, rather than asking one final LLM call to reproduce all of
    # them verbatim. Earlier versions asked the Report Writer agent to
    # combine and repeat every upstream section itself, but this proved
    # unreliable in practice - the LLM would sometimes condense or
    # silently drop entire sections (observed: Interview Questions and
    # Learning Roadmap missing from generated reports) despite explicit
    # instructions not to. Building the guaranteed sections directly from
    # each task's .output.raw removes that failure mode structurally: the
    # Report Writer's only job now is to synthesize the 2 genuinely new
    # sections (Career Advice, Overall Resume Score), not reproduce content
    # that already exists elsewhere.
    def _strip_code_fence(text: str) -> str:
        """
        Remove a leading/trailing triple-backtick code fence if the LLM
        wrapped its markdown output in one (e.g. ```markdown ... ``` or
        plain ``` ... ```). This is common LLM behavior when asked to
        produce "a markdown document" - without stripping it, Streamlit
        renders the entire section as a literal code block instead of
        parsed markdown (headings, bold, etc. all show as raw text).
        """
        text = text.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if lines:
                lines = lines[1:]  # drop opening ``` or ```markdown line
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]  # drop closing ```
            text = "\n".join(lines).strip()
        return text

    def _section(header: str, task) -> str:
        body = (task.output.raw if task.output else "").strip()
        body = _strip_code_fence(body)
        return f"## {header}\n\n{body}\n\n"

    synthesized = _strip_code_fence(report_task.output.raw if report_task.output else "")

    report_markdown = (
        _section("Resume Summary", resume_task)
        + _section("Skill Analysis", skill_task)
        + _section("Recommended Jobs", job_task)
        + _section("Interview Questions", interview_task)
        + _section("Learning Roadmap", roadmap_task)
        + synthesized
    ).strip()

    if not report_markdown:
        raise RuntimeError(
            "The crew completed but produced an empty report. This usually "
            "means one of the agents hit an error or rate limit mid-run - "
            "check the app logs for details."
        )

    report_id = save_report(resume_id=resume_id, report_markdown=report_markdown)

    # The raw uploaded PDF is no longer needed once its text has been
    # extracted and the report generated - both are already safely stored
    # in the database. Deleting it here minimizes how long a copy of the
    # candidate's original file sits on disk, reducing the data footprint
    # kept per user. Best-effort: if this fails for any reason, we don't
    # want to fail the whole analysis over a cleanup step.
    try:
        Path(resume_pdf_path).unlink(missing_ok=True)
    except OSError:
        pass

    return {
        "report_markdown": report_markdown,
        "resume_id": resume_id,
        "report_id": report_id,
    }
