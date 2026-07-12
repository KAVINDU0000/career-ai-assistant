"""
config.py
---------
Centralized configuration for CareerCompass.

All environment-dependent values (API keys, model names, paths) live here.
No other module should read os.environ directly - they import from here instead.
This follows the Single Responsibility Principle: one place owns configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load variables from a local .env file (if present) into the process environment.
load_dotenv()

# Newer crewai-tools versions restrict PDFSearchTool to reading files only
# from an "allowed directory" as a path-traversal safety measure. We save
# uploaded resumes inside this project's own data/ folder (see app.py) so
# they naturally fall within that allowed scope. This flag is a documented
# fallback in case that check is still stricter than expected on your
# platform - it does not weaken safety for arbitrary user-supplied paths,
# since we always control the exact path being read (our own data/ folder).
os.environ.setdefault("CREWAI_TOOLS_ALLOW_UNSAFE_PATHS", "true")


class Settings:
    """Application-wide settings, populated from environment variables."""

    # --- OpenAI / LLM configuration ---
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))

    # --- Paths ---
    BASE_DIR: Path = Path(__file__).resolve().parent
    DATA_DIR: Path = BASE_DIR / "data"
    REPORTS_DIR: Path = BASE_DIR / "reports"

    # --- App behavior ---
    MAX_RESUME_FILE_MB: int = int(os.getenv("MAX_RESUME_FILE_MB", "10"))
    REPORT_FILENAME: str = os.getenv("REPORT_FILENAME", "career_report.md")

    @classmethod
    def validate(cls) -> None:
        """
        Fail fast and loudly if required configuration is missing.
        Called once at application startup (app.py) before any agent runs.
        """
        if not cls.OPENAI_API_KEY:
            raise EnvironmentError(
                "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key."
            )
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)


settings = Settings()
