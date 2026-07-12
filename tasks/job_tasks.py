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
            "never recommend such roles by default.\n\n"
            "SALARY INSTRUCTIONS - read carefully:\n"
            "- Quote salary in the candidate's own local currency, using the "
            "PAY PERIOD that country actually advertises jobs in. Sri Lanka, "
            "India, and most South Asian markets advertise jobs with a "
            "MONTHLY salary figure, not annual - state 'per month' "
            "explicitly. Only use an annual figure for countries where that "
            "is the actual local convention (e.g. US, UK).\n"
            "- Do NOT calculate this by taking a global/US annual salary "
            "figure and converting it through an exchange rate - that "
            "produces wildly inflated numbers that don't reflect real local "
            "pay scales. Instead, reason directly from realistic local job "
            "market rates for that specific role, industry, and experience "
            "level in that country today.\n"
            "- For calibration in Sri Lanka specifically: an entry-level "
            "office/professional role typically pays roughly LKR "
            "40,000-90,000 per month; a mid-level experienced professional "
            "roughly LKR 100,000-250,000 per month; a senior specialist, "
            "manager, or director-level role roughly LKR 250,000-600,000+ "
            "per month. Use these only as an order-of-magnitude sanity "
            "check, not a rigid formula - adjust for the specific role and "
            "industry."
        ),
        expected_output=(
            "A Markdown table or list of 3-5 recommended jobs, each genuinely "
            "grounded in the candidate's field. For each job include: "
            "Matching Score (0-100), Reasoning citing specific resume "
            "evidence, Required Missing Skills, an approximate Salary Range "
            "in the candidate's own local currency AND correct local pay "
            "period (e.g. 'LKR 120,000 - 180,000 per month', not an inflated "
            "annual-equivalent figure), clearly labeled as an estimate, and "
            "Career Growth outlook."
        ),
        agent=agent,
        context=context,
    )
