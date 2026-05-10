# Architecture Overview

## Document Q&A Assistant

A Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions about their content using natural language.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| LLM | Groq (llama-3.3-70b-versatile) |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Vector Store | FAISS (in-memory) |
| Orchestration | LangChain |
| PDF Parsing | pdfplumber |
| DOCX Parsing | docx2txt |

---

## RAG Pipeline Flow

```
User uploads document
        │
        ▼
document_loader.py → Extract raw text (PDF / DOCX / TXT)
        │
        ▼
rag_pipeline.py → Split text into chunks (RecursiveCharacterTextSplitter)
        │
        ▼
HuggingFace Embeddings → Convert chunks to vectors
        │
        ▼
FAISS Vector Store → Store and index vectors
        │
        ▼
User asks a question
        │
        ▼
FAISS Retriever → Find top-K most relevant chunks
        │
        ▼
PromptTemplate → Combine context + question
        │
        ▼
Groq LLM → Generate answer
        │
        ▼
Streamlit UI → Display answer to user
```

---

## Project Structure

```
doc-qa-app/
├── src/
│   ├── __init__.py
│   ├── config.py            # All settings and constants
│   ├── document_loader.py   # Text extraction logic
│   └── rag_pipeline.py      # Core RAG logic
├── tests/
│   ├── __init__.py
│   ├── test_document_loader.py
│   └── test_rag_pipeline.py
├── docs/
│   └── architecture.md      # This file
├── app.py                   # Streamlit UI entry point
├── .env                     # Secret keys (not committed)
├── .env.example             # Template for contributors
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Configuration

All configurable values live in `src/config.py`:

- `MODEL_NAME` — Groq model to use
- `EMBEDDING_MODEL` — HuggingFace sentence transformer
- `CHUNK_SIZE` / `CHUNK_OVERLAP` — Text splitting parameters
- `TOP_K` — Number of chunks retrieved per query
- `MAX_TOKENS` — LLM response length limit
