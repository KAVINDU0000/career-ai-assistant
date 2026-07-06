"""
tests/test_pdf_tool.py
------------------------
Basic unit tests for tools/pdf_tool.py that don't require any API key or
network access - they only exercise the local PDF-parsing logic.

Run with: pytest tests/
"""

import sys
from pathlib import Path

import pytest
from pypdf import PdfWriter

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.pdf_tool import extract_resume_text  # noqa: E402


def _make_blank_pdf(path: Path) -> None:
    """Create a minimal, valid PDF with a single blank page (no text)."""
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    with open(path, "wb") as f:
        writer.write(f)


def test_extract_resume_text_missing_file_raises(tmp_path):
    missing_path = tmp_path / "does_not_exist.pdf"
    with pytest.raises(FileNotFoundError):
        extract_resume_text(str(missing_path))


def test_extract_resume_text_blank_pdf_raises_value_error(tmp_path):
    pdf_path = tmp_path / "blank.pdf"
    _make_blank_pdf(pdf_path)
    with pytest.raises(ValueError):
        extract_resume_text(str(pdf_path))
