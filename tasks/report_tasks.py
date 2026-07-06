"""
tasks/report_tasks.py
------------------------
Task for Agent 6 (Career Report Writer Agent).

This is the final task in the pipeline. It writes the combined report
directly to disk via CrewAI's `output_file` mechanism, so no manual
file-writing code is needed in app.py.
"""

from crewai import Task


def build_report_task(agent, context: list, output_path: str) -> Task:
    """
    Build the final career report task.

    Args:
        agent: The Career Report Writer Agent.
        context: List of every upstream Task (resume, skill, job,
            interview, roadmap) whose outputs get combined here.
        output_path: Absolute path to write career_report.md to.

    Returns:
        Configured Task instance.
    """
    return Task(
        description=(
            "Combine the resume summary, skill analysis, job matches, "
            "interview questions, and learning roadmap from all previous "
            "tasks into one cohesive, professional career report."
        ),
        expected_output=(
            "A complete Markdown document with these top-level sections, in "
            "this order: 'Resume Summary', 'Skill Analysis', 'Recommended "
            "Jobs', 'Interview Questions', 'Learning Roadmap', 'Career "
            "Advice', and 'Overall Resume Score' (a single score out of 100 "
            "with a one-paragraph justification). Use clear Markdown headers "
            "(##) for each section."
        ),
        agent=agent,
        context=context,
        output_file=output_path,
    )
