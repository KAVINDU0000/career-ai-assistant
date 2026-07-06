"""
tasks/job_tasks.py
---------------------
Task for Agent 3 (Job Matching Agent).
"""

from crewai import Task


def build_job_matching_task(agent, context: list) -> Task:
    """
    Build the job matching task.

    Args:
        agent: The Job Matching Agent.
        context: List of upstream Task objects this depends on
            (resume analysis + skill analysis).

    Returns:
        Configured Task instance.
    """
    return Task(
        description=(
            "Using the resume summary and skill report from previous tasks, "
            "first determine the candidate's actual professional field based "
            "on their education and experience (e.g. this could be IT, "
            "healthcare, finance, marketing, education, design, skilled "
            "trades, etc. - infer it from the resume, do not assume). Then "
            "recommend 3-5 job roles within or realistically adjacent to that "
            "field. Only recommend a technology or AI-related role if the "
            "candidate's resume actually demonstrates technical education, "
            "projects, or experience supporting it - never recommend such "
            "roles by default."
        ),
        expected_output=(
            "A Markdown table or list of 3-5 recommended jobs, each genuinely "
            "grounded in the candidate's field. For each job include: "
            "Matching Score (0-100), Reasoning citing specific resume "
            "evidence, Required Missing Skills, an approximate Salary Range "
            "(clearly labeled as an estimate), and Career Growth outlook."
        ),
        agent=agent,
        context=context,
    )
