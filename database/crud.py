"""
database/crud.py
-------------------
Small, focused functions for reading and writing Resume/Report rows.
Every function that touches resumes or reports takes a user_id and scopes
its query to that user - so one user can never see another's history.
"""

import re
from typing import Optional

from database.db import get_session
from database.models import Report, Resume


def save_resume(user_id: int, filename: str, raw_text: str) -> int:
    """
    Insert a new resume row owned by the given user.

    Args:
        user_id: id of the owning User.
        filename: Original uploaded filename (for display in History).
        raw_text: Extracted resume text.

    Returns:
        The new resume's id.
    """
    session = get_session()
    try:
        resume = Resume(user_id=user_id, filename=filename, raw_text=raw_text)
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


def get_all_reports(user_id: int) -> list[dict]:
    """
    Fetch every report belonging to the given user, most recent first.

    Args:
        user_id: Only reports whose resume belongs to this user are returned.

    Returns:
        List of dicts: {id, filename, created_at, overall_score, report_markdown}
    """
    session = get_session()
    try:
        rows = (
            session.query(Report, Resume)
            .join(Resume, Report.resume_id == Resume.id)
            .filter(Resume.user_id == user_id)
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


def get_report_by_id(user_id: int, report_id: int) -> Optional[dict]:
    """
    Fetch a single report by id, but only if it belongs to the given user.

    Args:
        user_id: The requesting user's id - enforces ownership.
        report_id: The report's primary key.

    Returns:
        A dict as in get_all_reports(), or None if not found or not owned
        by this user.
    """
    session = get_session()
    try:
        result = (
            session.query(Report, Resume)
            .join(Resume, Report.resume_id == Resume.id)
            .filter(Report.id == report_id, Resume.user_id == user_id)
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


def delete_report(user_id: int, report_id: int) -> bool:
    """
    Delete a single report by id, but only if it belongs to the given user.

    Args:
        user_id: The requesting user's id - enforces ownership.
        report_id: The report's primary key.

    Returns:
        True if a row was deleted, False if no matching, owned report existed.
    """
    session = get_session()
    try:
        report = (
            session.query(Report)
            .join(Resume, Report.resume_id == Resume.id)
            .filter(Report.id == report_id, Resume.user_id == user_id)
            .first()
        )
        if report is None:
            return False
        session.delete(report)
        session.commit()
        return True
    finally:
        session.close()
