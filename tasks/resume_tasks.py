"""
tasks/resume_tasks.py
-----------------------
Task for Agent 1 (Resume Analysis Agent).
"""

from crewai import Task


def build_resume_analysis_task(agent, resume_text_preview: str) -> Task:
    """
    Build the resume analysis task.

    Args:
        agent: The Resume Analysis Agent.
        resume_text_preview: Raw extracted text from the PDF, injected directly
            into the prompt as a guaranteed source of truth alongside the
            agent's PDFSearchTool.

    Returns:
        Configured Task instance.
    """
    return Task(
        description=(
            "Analyze the candidate's resume below and the attached PDF search "
            "tool to extract a complete structured summary.\n\n"
            "--- RAW RESUME TEXT (ground truth, may be imperfectly formatted) ---\n"
            f"{resume_text_preview}\n"
            "--- END RAW RESUME TEXT ---\n\n"
            "Do not invent information that isn't present. If a section is "
            "missing from the resume, state 'Not specified' rather than guessing."
        ),
        expected_output=(
            "A structured Markdown summary with these exact sections: "
            "Name, Education, Experience, Projects, Technical Skills, "
            "Soft Skills, Certifications, Achievements."
        ),
        agent=agent,
    )
