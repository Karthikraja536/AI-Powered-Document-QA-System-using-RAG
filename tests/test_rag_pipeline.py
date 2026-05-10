"""
test_rag_pipeline.py
--------------------
Unit tests for the RAGPipeline class.
"""

import pytest
from unittest.mock import MagicMock, patch


@patch("src.rag_pipeline.GROQ_API_KEY", "fake-key-for-testing")
@patch("src.rag_pipeline.HuggingFaceEmbeddings")
@patch("src.rag_pipeline.ChatGroq")
def test_pipeline_initializes(mock_groq, mock_embeddings):
    from src.rag_pipeline import RAGPipeline

    pipeline = RAGPipeline()
    assert pipeline.qa_chain is None
    assert pipeline.num_chunks == 0


@patch("src.rag_pipeline.GROQ_API_KEY", "fake-key-for-testing")
@patch("src.rag_pipeline.HuggingFaceEmbeddings")
@patch("src.rag_pipeline.ChatGroq")
@patch("src.rag_pipeline.FAISS")
def test_ingest_sets_num_chunks(mock_faiss, mock_groq, mock_embeddings):
    from src.rag_pipeline import RAGPipeline

    mock_faiss.from_texts.return_value = MagicMock(
        as_retriever=MagicMock(return_value=MagicMock())
    )

    pipeline = RAGPipeline()
    pipeline.ingest("This is a test document. " * 50)
    assert pipeline.num_chunks > 0


@patch("src.rag_pipeline.GROQ_API_KEY", "fake-key-for-testing")
@patch("src.rag_pipeline.HuggingFaceEmbeddings")
@patch("src.rag_pipeline.ChatGroq")
def test_ask_without_ingestion_returns_message(mock_groq, mock_embeddings):
    from src.rag_pipeline import RAGPipeline

    pipeline = RAGPipeline()
    result = pipeline.ask("What is this about?")
    assert "No document loaded" in result["answer"]
    assert result["sources"] == []


@patch("src.rag_pipeline.GROQ_API_KEY", None)
def test_missing_api_key_raises_error():
    from src.rag_pipeline import RAGPipeline

    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        RAGPipeline()
