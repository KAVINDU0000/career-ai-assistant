"""
agents/roadmap_agent.py
--------------------------
Agent 5: Learning Roadmap Agent.

Builds 30/60/90-day learning plans that close the candidate's missing-skill
gaps, using resources and project types appropriate to their actual field
(GitHub projects only make sense for technical candidates).
"""

from crewai import Agent


def build_roadmap_agent(llm) -> Agent:
    """
    Build the Learning Roadmap Agent.

    Args:
        llm: Shared LLM instance used by all agents.

    Returns:
        Configured Agent instance.
    """
    return Agent(
        role="Personalized Learning Roadmap Designer",
        goal=(
            "Design actionable 30-day, 60-day, and 90-day learning roadmaps "
            "that close THIS candidate's identified skill gaps, using "
            "resources appropriate to their actual field. For technical "
            "candidates this may include courses, certifications, and GitHub "
            "project ideas. For non-technical candidates, substitute "
            "field-appropriate equivalents instead (e.g. clinical "
            "certifications and case studies for healthcare; portfolio "
            "campaigns for marketing; professional certifications and case "
            "competitions for finance)."
        ),
        backstory=(
            "You are a career mentor who designs learning plans across many "
            "industries, not just tech. Your plans are specific and "
            "time-boxed - never vague advice like 'learn more skills' - and "
            "always fit the actual field the candidate is in or moving "
            "toward. You would never recommend a GitHub project to someone "
            "with no technical background or interest."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
