"""
Agents package.

Each module defines one CrewAI Agent with a narrow, well-defined responsibility.
build_all_agents() wires them together with a shared LLM, so crew.py only
needs one import.
"""

from crewai import LLM

from config import settings

from .resume_analysis_agent import build_resume_analysis_agent
from .skill_analysis_agent import build_skill_analysis_agent
from .job_matching_agent import build_job_matching_agent
from .interview_prep_agent import build_interview_prep_agent
from .roadmap_agent import build_roadmap_agent
from .report_writer_agent import build_report_writer_agent


def build_all_agents() -> dict:
    """
    Construct every agent needed for one end-to-end run.

    Returns:
        A dict mapping a short name to its Agent instance, e.g.
        {"resume_analyst": Agent(...), "skill_analyst": Agent(...), ...}
    """
    llm = LLM(
        model=f"openai/{settings.OPENAI_MODEL_NAME}",
        temperature=settings.LLM_TEMPERATURE,
        api_key=settings.OPENAI_API_KEY,
    )

    return {
        "resume_analyst": build_resume_analysis_agent(llm),
        "skill_analyst": build_skill_analysis_agent(llm),
        "job_matcher": build_job_matching_agent(llm),
        "interview_coach": build_interview_prep_agent(llm),
        "roadmap_planner": build_roadmap_agent(llm),
        "report_writer": build_report_writer_agent(llm),
    }
