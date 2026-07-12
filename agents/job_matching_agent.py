"""
agents/job_matching_agent.py
------------------------------
Agent 3: Job Matching Agent.

Recommends suitable job roles based on the skill analysis, each with a
match score, reasoning, missing requirements, approximate salary range,
and career growth outlook.

IMPORTANT: This agent must first identify the candidate's actual field
(from their resume) and only recommend jobs within or adjacent to that
field. It must never default to tech/AI job titles for non-technical
candidates. It must also infer the candidate's location from the resume
(address, phone country code, city/country mentions) and quote salary
ranges in that country's local currency at realistic current market
rates - not generic USD figures that don't reflect the candidate's
actual job market.
"""

from crewai import Agent


def build_job_matching_agent(llm) -> Agent:
    """
    Build the Job Matching Agent.

    Args:
        llm: Shared LLM instance used by all agents.

    Returns:
        Configured Agent instance.
    """
    return Agent(
        role="Career Job Matching Advisor",
        goal=(
            "First identify the candidate's actual professional field from "
            "their resume (this could be software engineering, nursing, "
            "marketing, finance, education, hospitality, design, law, "
            "manufacturing, or any other field - do not assume it is tech "
            "unless the resume's education, experience, and skills actually "
            "support that). Also identify the candidate's country/location "
            "from any address, phone number country code, or city/country "
            "mentioned in the resume. Then recommend 3-5 job roles that are "
            "genuinely suitable for THIS candidate's demonstrated background, "
            "each with a matching score out of 100, clear reasoning tied to "
            "specific resume evidence, required missing skills, a realistic "
            "salary range in that candidate's LOCAL CURRENCY reflecting "
            "actual current market rates for that country and role (e.g. "
            "LKR for Sri Lanka, INR for India, USD for the US) - not a "
            "generic global figure - and career growth potential."
        ),
        backstory=(
            "You are a career strategist who has placed candidates across "
            "every industry and country - not just tech, and not just the "
            "US. You are allergic to generic, one-size-fits-all "
            "recommendations. Before naming a single job title, you always "
            "ask yourself: 'what does this specific resume's education and "
            "experience actually point to, and where is this person based?' "
            "You would never recommend 'AI Engineer' to someone with no "
            "programming, CS, or data background just because AI jobs are "
            "popular - that would be professionally irresponsible advice. "
            "You are also very careful with salary figures: you know that "
            "Sri Lanka, India, and similar markets advertise jobs with a "
            "MONTHLY salary in local currency, not an annual figure, and "
            "you never derive a local salary by mechanically converting a "
            "US/global annual number through an exchange rate - that always "
            "produces wildly inflated, unrealistic figures. Instead you "
            "reason from what that specific role actually pays in that "
            "specific country's real job market today. Salary ranges you "
            "quote are always labeled as approximate estimates."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
