"""
agents/resume_analysis_agent.py
--------------------------------
Agent 1: Resume Analysis Agent.

Responsible for producing a structured resume summary (education,
experience, projects, skills, certifications, achievements) that every
downstream agent will rely on.

No PDF search tool is attached - the full resume text is already injected
directly into this agent's task prompt (see tasks/resume_tasks.py), which
is both simpler and far lighter on CPU/memory than building a live vector
embedding index per upload. This matters especially on resource-constrained
hosting (e.g. Streamlit Community Cloud's free tier), where a RAG tool's
embedding step was found to be the primary cause of failed/incomplete runs.
"""

from crewai import Agent


def build_resume_analysis_agent(llm) -> Agent:
    """
    Build the Resume Analysis Agent.

    Args:
        llm: Shared LLM instance used by all agents.

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
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
