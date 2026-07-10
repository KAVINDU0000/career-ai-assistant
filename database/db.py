"""
database/db.py
-----------------
Creates the SQLite engine and session factory, and exposes init_db() to
create tables on first run.

Using SQLite here (a single local file, career_assistant.db) keeps setup
at zero - no separate database server to install or configure. The models
are written in plain SQLAlchemy, so swapping to PostgreSQL later only
requires changing DATABASE_URL - no other code changes needed.
"""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from database.models import Base

DB_PATH = settings.BASE_DIR / "career_assistant.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# check_same_thread=False is needed because Streamlit can call into the DB
# from a different thread than the one that created the connection.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    """Create all tables if they don't already exist. Safe to call every startup."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """
    Return a new SQLAlchemy session.

    Callers are responsible for closing the session (or use it as a
    context manager) once they're done with it.
    """
    return SessionLocal()
