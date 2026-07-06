"""
tasks/interview_tasks.py
---------------------------
Task for Agent 4 (Interview Preparation Agent).
"""

from crewai import Task


def build_interview_prep_task(agent, context: list) -> Task:
    """
    Build the interview preparation task.

    Args:
        agent: The Interview Preparation Agent.
        context: List of upstream Task objects this depends on
            (resume analysis + skill analysis).

    Returns:
        Configured Task instance.
    """
    return Task(
        description=(
            "Using the candidate's resume summary and skill report, generate "
            "interview questions grounded in their actual field, projects, and "
            "stated skills. If the resume is technical, cover relevant "
            "technical topics (Programming Languages, Machine Learning, Deep "
            "Learning, Generative AI, SQL, etc. as applicable). If the resume "
            "is in a different field, generate questions genuinely relevant "
            "to that field's real interview practices instead. Always add a "
            "separate 'Behavioral Questions' section. Tag every question with "
            "a difficulty level."
        ),
        expected_output=(
            "A Markdown list of at least 15 interview questions grouped by "
            "topic relevant to the candidate's actual field, each tagged "
            "[Easy], [Medium], or [Hard], plus a separate 'Behavioral "
            "Questions' section with at least 5 questions."
        ),
        agent=agent,
        context=context,
    )
