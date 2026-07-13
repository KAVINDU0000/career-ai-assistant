"""
tasks/report_tasks.py
------------------------
Task for Agent 6 (Career Report Writer Agent).

IMPORTANT DESIGN NOTE: this task now ONLY produces the 'Career Advice' and
'Overall Resume Score' sections. The other 5 sections (Resume Summary,
Skill Analysis, Recommended Jobs, Interview Questions, Learning Roadmap)
are assembled programmatically in crew.py directly from each upstream
task's own output - not regenerated or re-summarized here.

This exists because the previous approach (asking this agent to combine
and reproduce all 5 upstream sections verbatim) was unreliable in
practice: the LLM would sometimes condense, shorten, or silently drop
entire sections (observed: Interview Questions and Learning Roadmap
missing from generated reports) despite explicit instructions not to.
Having this agent only write 2 new, genuinely synthesized sections - and
letting code guarantee the other 5 are always present - removes that
failure mode structurally rather than trying to prompt around it.
"""

from crewai import Task


def build_report_task(agent, context: list) -> Task:
    """
    Build the final task: writing Career Advice and an Overall Resume Score.

    Args:
        agent: The Career Report Writer Agent.
        context: List of every upstream Task (resume, skill, job,
            interview, roadmap) whose outputs inform this synthesis.

    Returns:
        Configured Task instance.
    """
    return Task(
        description=(
            "You have been given the full resume summary, skill analysis, "
            "job matches, interview questions, and learning roadmap from "
            "previous tasks as context. Using all of that as background, "
            "write two NEW sections that synthesize genuine insight across "
            "everything you've seen - do not repeat or copy the upstream "
            "content itself, it will be included separately."
        ),
        expected_output=(
            "A Markdown document with EXACTLY these 2 top-level sections, "
            "in this order:\n"
            "## Career Advice\n"
            "(2-3 paragraphs of genuinely synthesized, specific career "
            "guidance for this candidate, drawing on everything in context)\n"
            "## Overall Resume Score\n"
            "(a single score out of 100, e.g. 'Score: 78/100', followed by "
            "a one-paragraph justification referencing specific strengths "
            "and gaps from the resume)"
        ),
        agent=agent,
        context=context,
        # NOTE: output_file intentionally omitted. CrewAI's output_file
        # mechanism has a documented history of silently failing to write
        # depending on version/environment (see crewAI GitHub issues #1707,
        # #1803, #3066). Instead, crew.py reads this task's raw output
        # directly and combines it with the other 5 sections programmatically.
    )
