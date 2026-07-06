"""
tools/pdf_tool.py
------------------
Wraps CrewAI's built-in PDFSearchTool (RAG-based semantic search over a PDF)
and adds a plain-text extraction helper for cases where agents need the
full resume text rather than a similarity-searched snippet.

Why both?
- PDFSearchTool: lets the Resume Analysis Agent ask targeted questions
  ("What programming languages are mentioned?") using retrieval-augmented
  generation instead of dumping the whole PDF into the prompt.
- extract_resume_text: a deterministic, non-LLM fallback used by app.py
  to show a raw preview and to guarantee the crew always has the full
  text available, even if RAG retrieval misses something.
"""

from pathlib import Path

from pypdf import PdfReader

from config import settings


def get_resume_search_tool(pdf_path: str):
    """
    Build a PDFSearchTool scoped to a single resume file.

    The crewai_tools import is done lazily inside this function (rather than
    at module level) so that extract_resume_text() below - a plain PDF
    utility with no CrewAI dependency - can be imported and unit-tested
    without requiring the full crewai_tools package to be installed.

    Args:
        pdf_path: Absolute path to the uploaded resume PDF.

    Returns:
        A configured PDFSearchTool instance ready to be attached to an agent.

    Raises:
        FileNotFoundError: if the given path does not exist.
    """
    from crewai_tools import PDFSearchTool

    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"Resume PDF not found at: {pdf_path}")

    return PDFSearchTool(
        pdf=str(path),
        config=dict(
            llm=dict(
                provider="openai",
                config=dict(model=settings.OPENAI_MODEL_NAME),
            ),
            embedder=dict(
                provider="openai",
                config=dict(model="text-embedding-3-small"),
            ),
        ),
    )


def extract_resume_text(pdf_path: str) -> str:
    """
    Extract raw text from every page of the resume PDF.

    This is intentionally simple and dependency-light (no LLM calls) so it
    can be used for previews and as a guaranteed fallback source of truth.

    Args:
        pdf_path: Absolute path to the uploaded resume PDF.

    Returns:
        The concatenated text of all pages, separated by double newlines.

    Raises:
        FileNotFoundError: if the given path does not exist.
        ValueError: if no extractable text is found (e.g. a scanned image PDF).
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"Resume PDF not found at: {pdf_path}")

    reader = PdfReader(str(path))
    pages_text = [page.extract_text() or "" for page in reader.pages]
    full_text = "\n\n".join(pages_text).strip()

    if not full_text:
        raise ValueError(
            "No extractable text found in the PDF. "
            "It may be a scanned image - try a text-based PDF export instead."
        )

    return full_text
