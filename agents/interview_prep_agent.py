"""
agents/interview_prep_agent.py
---------------------------------
Agent 4: Interview Preparation Agent.

Generates interview questions tailored to the candidate's actual projects,
experience, and field - technical topics only where the resume actually
supports them - plus behavioral questions, each tagged with a difficulty level.
"""

from crewai import Agent


def build_interview_prep_agent(llm) -> Agent:
    """
    Build the Interview Preparation Agent.

    Args:
        llm: Shared LLM instance used by all agents.

    Returns:
        Configured Agent instance.
    """
    return Agent(
        role="Interview Coach",
        goal=(
            "Generate a well-rounded set of interview questions personalized "
            "to THIS candidate's actual field, projects, and experience. If "
            "the resume shows a technical/software/AI background, include "
            "relevant technical topics (e.g. programming languages, ML/DL, "
            "SQL). If the resume shows a different field (healthcare, "
            "finance, marketing, education, trades, etc.), generate "
            "questions specific to THAT field's real interview practices "
            "instead. Always include a Behavioral Questions section, and "
            "label every question Easy, Medium, or Hard."
        ),
        backstory=(
            "You are a hiring manager who has run interview panels across "
            "many industries, not just tech. You always ask: 'what job is "
            "this specific person actually applying for based on their "
            "resume?' before writing a single question. You would never hand "
            "a nurse a Python coding question - that would embarrass "
            "everyone involved."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
