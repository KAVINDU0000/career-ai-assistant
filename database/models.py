"""
database/models.py
--------------------
SQLAlchemy ORM models for persisting resumes and their generated reports.

Schema:
    resumes (id, filename, uploaded_at, raw_text)
    reports (id, resume_id -> resumes.id, report_markdown, overall_score, created_at)

One resume can have multiple reports over time (e.g. if you re-run analysis
on the same file, or add versioning later) - that's why it's a foreign key
relationship rather than one flat table.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Base class all ORM models inherit from."""
    pass


class Resume(Base):
    """A single uploaded resume file and its extracted text."""

    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    raw_text = Column(Text, nullable=False)

    reports = relationship("Report", back_populates="resume", cascade="all, delete-orphan")


class Report(Base):
    """A generated career report tied to one resume."""

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    report_markdown = Column(Text, nullable=False)
    overall_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    resume = relationship("Resume", back_populates="reports")
