"""
database/crud.py
-------------------
Small, focused functions for reading and writing Resume/Report rows.
Keeping these separate from db.py and models.py follows the same
Single Responsibility pattern used throughout this project: models define
shape, db.py defines connection plumbing, crud.py defines operations.
"""

import re
from typing import Optional

from database.db import get_session
from database.models import Report, Resume


def save_resume(filename: str, raw_text: str) -> int:
    """
    Insert a new resume row.

    Args:
        filename: Original uploaded filename (for display in History).
        raw_text: Extracted resume text.

    Returns:
        The new resume's id.
    """
    session = get_session()
    try:
        resume = Resume(filename=filename, raw_text=raw_text)
        session.add(resume)
        session.commit()
        session.refresh(resume)
        return resume.id
    finally:
        session.close()


def _extract_overall_score(report_markdown: str) -> Optional[float]:
    """
    Best-effort extraction of the numeric score from the report's
    'Overall Resume Score' section (e.g. "78/100" -> 78.0).

    Returns None if no score pattern is found, rather than raising -
    the score is a nice-to-have for sorting/display, not critical data.
    """
    match = re.search(r"(\d{1,3})\s*/\s*100", report_markdown)
    if match:
        return float(match.group(1))
    return None


def save_report(resume_id: int, report_markdown: str) -> int:
    """
    Insert a new report row linked to a resume.

    Args:
        resume_id: id of the parent Resume row.
        report_markdown: Full generated report text.

    Returns:
        The new report's id.
    """
    session = get_session()
    try:
        report = Report(
            resume_id=resume_id,
            report_markdown=report_markdown,
            overall_score=_extract_overall_score(report_markdown),
        )
        session.add(report)
        session.commit()
        session.refresh(report)
        return report.id
    finally:
        session.close()


def get_all_reports() -> list[dict]:
    """
    Fetch every report, most recent first, joined with its resume's filename.

    Returns:
        List of dicts: {id, filename, created_at, overall_score, report_markdown}
    """
    session = get_session()
    try:
        rows = (
            session.query(Report, Resume)
            .join(Resume, Report.resume_id == Resume.id)
            .order_by(Report.created_at.desc())
            .all()
        )
        return [
            {
                "id": report.id,
                "filename": resume.filename,
                "created_at": report.created_at,
                "overall_score": report.overall_score,
                "report_markdown": report.report_markdown,
            }
            for report, resume in rows
        ]
    finally:
        session.close()


def get_report_by_id(report_id: int) -> Optional[dict]:
    """
    Fetch a single report by id, joined with its resume's filename.

    Args:
        report_id: The report's primary key.

    Returns:
        A dict as in get_all_reports(), or None if not found.
    """
    session = get_session()
    try:
        result = (
            session.query(Report, Resume)
            .join(Resume, Report.resume_id == Resume.id)
            .filter(Report.id == report_id)
            .first()
        )
        if result is None:
            return None
        report, resume = result
        return {
            "id": report.id,
            "filename": resume.filename,
            "created_at": report.created_at,
            "overall_score": report.overall_score,
            "report_markdown": report.report_markdown,
        }
    finally:
        session.close()


def delete_report(report_id: int) -> bool:
    """
    Delete a single report by id (leaves the resume row untouched).

    Args:
        report_id: The report's primary key.

    Returns:
        True if a row was deleted, False if no matching report existed.
    """
    session = get_session()
    try:
        report = session.query(Report).filter(Report.id == report_id).first()
        if report is None:
            return False
        session.delete(report)
        session.commit()
        return True
    finally:
        session.close()
