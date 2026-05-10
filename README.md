# 🤖 AI-Powered Document Q&A System using RAG

A Retrieval-Augmented Generation (RAG) web application that lets you upload documents and ask questions about their content in natural language — powered by **Groq LLM**, **HuggingFace Embeddings**, and **FAISS**.

---

## ✨ Features

- 📁 Upload **PDF, DOCX, DOC, or TXT** files
- 🔍 Semantic search using FAISS vector store
- 🤖 Fast answers powered by **Groq (llama-3.3-70b-versatile)**
- 💬 Chat-style interface with conversation history
- 🔒 API keys managed securely via `.env`

---

## 🗂️ Project Structure

```
AI-Powered Document Q&A System using RAG/
├── src/
│   ├── __init__.py
│   ├── config.py            # All settings and constants
│   ├── document_loader.py   # Text extraction (PDF, DOCX, TXT)
│   └── rag_pipeline.py      # Core RAG logic
├── tests/
│   ├── __init__.py
│   ├── test_document_loader.py
│   └── test_rag_pipeline.py
├── docs/
│   └── architecture.md      # System design overview
├── app.py                   # Streamlit UI entry point
├── .env.example             # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ai-powered-doc-qa-rag.git
cd "AI-Powered Document Q&A System using RAG"
```

Or navigate manually:
```
Desktop → Projects → AI-Powered Document Q&A System using RAG
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Then open `.env` and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key at: https://console.groq.com/keys

### 5. Run the app
```bash
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## ⚙️ Configuration

All settings are centralized in `src/config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `MODEL_NAME` | `llama-3.3-70b-versatile` | Groq LLM model |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | HuggingFace sentence transformer |
| `CHUNK_SIZE` | `600` | Characters per text chunk |
| `CHUNK_OVERLAP` | `80` | Overlap between chunks |
| `TOP_K` | `4` | Retrieved chunks per query |
| `MAX_TOKENS` | `500` | Max LLM response length |

---

## 📖 How It Works

```
User uploads document
        │
        ▼
Extract raw text (PDF / DOCX / TXT)
        │
        ▼
Split into overlapping chunks
        │
        ▼
Embed chunks → Store in FAISS vector store
        │
        ▼
User asks a question
        │
        ▼
Retrieve top-K relevant chunks
        │
        ▼
Groq LLM generates answer from context
        │
        ▼
Display answer in chat UI
```

See [docs/architecture.md](docs/architecture.md) for the full system design.

---

## 📝 Notes

- The app answers **only from the uploaded document** — it won't hallucinate outside information
- FAISS vector store is **in-memory** — re-upload your document after restarting the app
- Transformer startup warnings in the console are harmless. To suppress them, add this to your `.env`:
  ```
  TRANSFORMERS_VERBOSITY=error
  ```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| UI | Streamlit |
| LLM | Groq (llama-3.3-70b-versatile) |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Vector Store | FAISS (in-memory) |
| Orchestration | LangChain |
| PDF Parsing | pdfplumber |
| DOCX Parsing | docx2txt |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
