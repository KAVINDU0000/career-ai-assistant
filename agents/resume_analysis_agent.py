"""
agents/resume_analysis_agent.py
--------------------------------
Agent 1: Resume Analysis Agent.

Responsible for reading the uploaded PDF and producing a structured
resume summary (education, experience, projects, skills, certifications,
achievements) that every downstream agent will rely on.
"""

from crewai import Agent


def build_resume_analysis_agent(llm, resume_tool) -> Agent:
    """
    Build the Resume Analysis Agent.

    Args:
        llm: Shared LLM instance used by all agents.
        resume_tool: A PDFSearchTool scoped to the uploaded resume.

    Returns:
        Configured Agent instance.
    """
    return Agent(
        role="Resume Analysis Specialist",
        goal=(
            "Extract a complete, accurate, structured summary of the candidate's "
            "resume, including name, education, experience, projects, technical "
            "skills, soft skills, certifications, and achievements."
        ),
        backstory=(
            "You are a meticulous technical recruiter with 15 years of experience "
            "screening resumes for top tech companies. You never invent information "
            "that is not in the document, and you flag ambiguity rather than guessing."
        ),
        tools=[resume_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
