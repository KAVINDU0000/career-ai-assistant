"""
tasks/skill_tasks.py
-----------------------
Task for Agent 2 (Skill Analysis Agent).
"""

from crewai import Task


def build_skill_analysis_task(agent, context: list) -> Task:
    """
    Build the skill analysis task.

    Args:
        agent: The Skill Analysis Agent.
        context: List of upstream Task objects this depends on
            (the resume analysis task).

    Returns:
        Configured Task instance.
    """
    return Task(
        description=(
            "Using the structured resume summary produced by the previous "
            "task, identify the candidate's strengths, weaknesses, and "
            "missing skills. First determine the candidate's actual field "
            "from their resume, then choose 5-7 skill categories that "
            "genuinely fit that field (do not default to software/AI "
            "categories unless the resume itself is technical). Always "
            "include Communication and Leadership as two of the categories."
        ),
        expected_output=(
            "A detailed Markdown skill report with sections: Strengths, "
            "Weaknesses, Missing Skills, and a Skill Categories breakdown "
            "using categories genuinely relevant to this candidate's field."
        ),
        agent=agent,
        context=context,
    )
