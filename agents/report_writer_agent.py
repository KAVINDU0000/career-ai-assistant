"""
agents/report_writer_agent.py
--------------------------------
Agent 6: Career Report Writer Agent.

Combines the outputs of every previous agent into a single, polished
career_report.md with a clear structure and an overall resume score.
"""

from crewai import Agent


def build_report_writer_agent(llm) -> Agent:
    """
    Build the Career Report Writer Agent.

    Args:
        llm: Shared LLM instance used by all agents.

    Returns:
        Configured Agent instance.
    """
    return Agent(
        role="Career Report Writer",
        goal=(
            "Synthesize the resume summary, skill analysis, job matches, "
            "interview questions, and learning roadmap into one polished "
            "Markdown career report with a clear structure and an overall "
            "resume score out of 100."
        ),
        backstory=(
            "You are a professional technical writer who produces "
            "recruiter-quality career reports. You write in clear, confident, "
            "encouraging language while staying factually grounded in the "
            "upstream analysis - never inventing details."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
