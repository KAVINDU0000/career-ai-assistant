"""
Tasks package.

build_all_tasks() wires every Task to its Agent and declares the `context`
(i.e. which earlier tasks' outputs it depends on), producing the linear
pipeline described in the project's TASK FLOW.
"""

from .resume_tasks import build_resume_analysis_task
from .skill_tasks import build_skill_analysis_task
from .job_tasks import build_job_matching_task
from .interview_tasks import build_interview_prep_task
from .roadmap_tasks import build_roadmap_task
from .report_tasks import build_report_task


def build_all_tasks(agents: dict, resume_text_preview: str, report_output_path: str) -> list:
    """
    Construct every task in pipeline order.

    Args:
        agents: dict of agent name -> Agent, from agents.build_all_agents().
        resume_text_preview: Raw extracted resume text, given as extra
            grounding context to the first task.
        report_output_path: Absolute path where the final report should be
            written to disk by the last task.

    Returns:
        Ordered list of Task objects, ready to hand to crewai.Crew(tasks=...).
    """
    resume_task = build_resume_analysis_task(agents["resume_analyst"], resume_text_preview)
    skill_task = build_skill_analysis_task(agents["skill_analyst"], context=[resume_task])
    job_task = build_job_matching_task(agents["job_matcher"], context=[resume_task, skill_task])
    interview_task = build_interview_prep_task(agents["interview_coach"], context=[resume_task, skill_task])
    roadmap_task = build_roadmap_task(agents["roadmap_planner"], context=[skill_task, job_task])
    report_task = build_report_task(
        agents["report_writer"],
        context=[resume_task, skill_task, job_task, interview_task, roadmap_task],
    )

    return [resume_task, skill_task, job_task, interview_task, roadmap_task, report_task]
