"""
config.py
---------
Centralized configuration for the Document Q&A App.
All constants and environment variables are managed here.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env for local development
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# --- Read GROQ_API_KEY from env or Streamlit secrets ---
def _get_groq_api_key() -> str | None:
    # 1. Try environment variable first (local .env or system env)
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key
    # 2. Fallback to Streamlit Cloud secrets
    try:
        import streamlit as st
        return st.secrets.get("GROQ_API_KEY")
    except Exception:
        return None

GROQ_API_KEY = _get_groq_api_key()

# --- LLM Settings ---
MODEL_NAME = "llama-3.3-70b-versatile"
MAX_TOKENS = 500
TEMPERATURE = 0

# --- Embedding Settings ---
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# --- Chunking Settings ---
CHUNK_SIZE = 600
CHUNK_OVERLAP = 80
CHUNK_SEPARATORS = ["\n\n", "\n", ".", " ", ""]

# --- Retrieval Settings ---
TOP_K = 4

# --- Supported File Types ---
SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".doc", ".txt"]

# --- Prompt Template ---
PROMPT_TEMPLATE = """
You are a helpful assistant that answers questions based strictly on the provided document context.

Context from document:
{context}

Question: {question}

Instructions:
- Answer using ONLY the information from the context above.
- If the answer is not in the context, say "I couldn't find that in the document."
- Be concise and clear.

Answer:
"""