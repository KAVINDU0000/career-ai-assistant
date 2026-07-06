"""
tasks/roadmap_tasks.py
-------------------------
Task for Agent 5 (Learning Roadmap Agent).
"""

from crewai import Task


def build_roadmap_task(agent, context: list) -> Task:
    """
    Build the learning roadmap task.

    Args:
        agent: The Learning Roadmap Agent.
        context: List of upstream Task objects this depends on
            (skill analysis + job matching).

    Returns:
        Configured Task instance.
    """
    return Task(
        description=(
            "Using the skill report and recommended jobs from previous tasks, "
            "design a personalized learning roadmap that closes the "
            "candidate's identified skill gaps, structured into 30-day, "
            "60-day, and 90-day phases. Use resources and practice activities "
            "genuinely appropriate to the candidate's actual field."
        ),
        expected_output=(
            "A Markdown roadmap with three clearly labeled phases (30/60/90 "
            "days). Each phase must list: specific Courses, Books/Resources, "
            "hands-on Projects or Practice Activities appropriate to the "
            "candidate's field, and relevant Certifications. Include a "
            "GitHub project idea only if the candidate's field is technical."
        ),
        agent=agent,
        context=context,
    )
