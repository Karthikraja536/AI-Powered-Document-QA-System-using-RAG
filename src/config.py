"""
config.py
---------
Centralized configuration for the Document Q&A App.
All constants and environment variables are managed here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

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
