"""
document_loader.py
------------------
Handles text extraction from uploaded documents.
Supports PDF, DOCX, DOC, and TXT formats.
"""

import os
import tempfile
from pathlib import Path

import pdfplumber
import docx2txt

from src.config import SUPPORTED_EXTENSIONS


def extract_text(uploaded_file) -> str | None:
    """
    Extracts plain text from an uploaded Streamlit file object.

    Args:
        uploaded_file: Streamlit UploadedFile object.

    Returns:
        Extracted text as a string, or None if unsupported/failed.
    """
    file_ext = Path(uploaded_file.name).suffix.lower()

    if file_ext not in SUPPORTED_EXTENSIONS:
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        if file_ext == ".pdf":
            return _extract_pdf(tmp_path)
        elif file_ext in [".docx", ".doc"]:
            return _extract_docx(tmp_path)
        elif file_ext == ".txt":
            return _extract_txt(tmp_path)
    finally:
        os.unlink(tmp_path)


def _extract_pdf(path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def _extract_docx(path: str) -> str:
    """Extract text from a DOCX/DOC file."""
    return docx2txt.process(path)


def _extract_txt(path: str) -> str:
    """Extract text from a plain TXT file."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
