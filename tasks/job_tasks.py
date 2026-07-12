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
            "trades, etc. - infer it from the resume, do not assume). Also "
            "determine the candidate's country/location from any address, "
            "phone number country code (e.g. +94 = Sri Lanka, +91 = India, "
            "+1 = US/Canada), or city/country explicitly mentioned in the "
            "resume. Then recommend 3-5 job roles within or realistically "
            "adjacent to that field. Only recommend a technology or "
            "AI-related role if the candidate's resume actually demonstrates "
            "technical education, projects, or experience supporting it - "
            "never recommend such roles by default. For each recommended "
            "job, quote the salary range in the candidate's own local "
            "currency (e.g. LKR for Sri Lanka, INR for India, USD only for "
            "US-based candidates) using realistic current market rates for "
            "that specific country, role, and experience level - do not "
            "default to USD or generic global figures if the candidate is "
            "clearly based elsewhere."
        ),
        expected_output=(
            "A Markdown table or list of 3-5 recommended jobs, each genuinely "
            "grounded in the candidate's field. For each job include: "
            "Matching Score (0-100), Reasoning citing specific resume "
            "evidence, Required Missing Skills, an approximate Salary Range "
            "in the candidate's own local currency reflecting realistic "
            "current market rates for their country (clearly labeled as an "
            "estimate), and Career Growth outlook."
        ),
        agent=agent,
        context=context,
    )
