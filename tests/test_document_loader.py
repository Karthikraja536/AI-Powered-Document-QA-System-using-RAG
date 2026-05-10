"""
test_document_loader.py
-----------------------
Unit tests for the document_loader module.
"""

import io
import pytest
from unittest.mock import MagicMock, patch


class MockUploadedFile:
    """Mimics a Streamlit UploadedFile object for testing."""

    def __init__(self, name: str, content: bytes):
        self.name = name
        self._content = content

    def read(self):
        return self._content


def test_extract_txt():
    from src.document_loader import extract_text

    content = b"Hello, this is a test document."
    mock_file = MockUploadedFile("test.txt", content)
    result = extract_text(mock_file)
    assert result is not None
    assert "Hello" in result


def test_unsupported_format_returns_none():
    from src.document_loader import extract_text

    mock_file = MockUploadedFile("test.xyz", b"some content")
    result = extract_text(mock_file)
    assert result is None


def test_empty_txt_returns_empty_string():
    from src.document_loader import extract_text

    mock_file = MockUploadedFile("empty.txt", b"")
    result = extract_text(mock_file)
    assert result == "" or result is None
