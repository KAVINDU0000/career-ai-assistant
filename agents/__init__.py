"""
Agents package.

Each module defines one CrewAI Agent with a narrow, well-defined responsibility.
build_all_agents() wires them together with a shared LLM and the resume tool,
so crew.py only needs one import.
"""

from crewai import LLM

from config import settings
from tools import get_resume_search_tool

from .resume_analysis_agent import build_resume_analysis_agent
from .skill_analysis_agent import build_skill_analysis_agent
from .job_matching_agent import build_job_matching_agent
from .interview_prep_agent import build_interview_prep_agent
from .roadmap_agent import build_roadmap_agent
from .report_writer_agent import build_report_writer_agent


def build_all_agents(resume_pdf_path: str) -> dict:
    """
    Construct every agent needed for one end-to-end run.

    Args:
        resume_pdf_path: Path to the uploaded resume PDF, needed by the
            Resume Analysis Agent's PDF search tool.

    Returns:
        A dict mapping a short name to its Agent instance, e.g.
        {"resume_analyst": Agent(...), "skill_analyst": Agent(...), ...}
    """
    llm = LLM(
        model=f"openai/{settings.OPENAI_MODEL_NAME}",
        temperature=settings.LLM_TEMPERATURE,
        api_key=settings.OPENAI_API_KEY,
    )
    resume_tool = get_resume_search_tool(resume_pdf_path)

    return {
        "resume_analyst": build_resume_analysis_agent(llm, resume_tool),
        "skill_analyst": build_skill_analysis_agent(llm),
        "job_matcher": build_job_matching_agent(llm),
        "interview_coach": build_interview_prep_agent(llm),
        "roadmap_planner": build_roadmap_agent(llm),
        "report_writer": build_report_writer_agent(llm),
    }
