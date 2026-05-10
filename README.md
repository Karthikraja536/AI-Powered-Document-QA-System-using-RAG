# 📄 Document Q&A Assistant

A RAG-powered (Retrieval-Augmented Generation) web app that lets you upload documents and ask questions about their content in natural language.

Built with **Streamlit**, **Groq LLM**, **HuggingFace Embeddings**, and **FAISS**.

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
doc-qa-app/
├── src/
│   ├── config.py            # All settings and constants
│   ├── document_loader.py   # Text extraction (PDF, DOCX, TXT)
│   └── rag_pipeline.py      # Core RAG logic
├── tests/
│   ├── test_document_loader.py
│   └── test_rag_pipeline.py
├── docs/
│   └── architecture.md      # System design overview
├── app.py                   # Streamlit UI entry point
├── .env.example             # Template for environment variables
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/doc-qa-app.git
cd doc-qa-app
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

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## ⚙️ Configuration

All settings are in `src/config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `MODEL_NAME` | `llama-3.3-70b-versatile` | Groq LLM model |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | HuggingFace embeddings |
| `CHUNK_SIZE` | `600` | Characters per text chunk |
| `CHUNK_OVERLAP` | `80` | Overlap between chunks |
| `TOP_K` | `4` | Retrieved chunks per query |
| `MAX_TOKENS` | `500` | Max LLM response length |

---

## 📖 How It Works

1. **Upload** a document → text is extracted
2. **Text is chunked** into overlapping segments
3. **Chunks are embedded** using HuggingFace and stored in FAISS
4. **User asks a question** → top-K relevant chunks are retrieved
5. **Groq LLM** generates an answer based only on retrieved context

See [docs/architecture.md](docs/architecture.md) for a detailed flow diagram.

---

## 📝 Notes

- The app answers **only from the uploaded document** — it won't hallucinate outside information
- Transformers startup warnings in the console are harmless; suppress them by adding `TRANSFORMERS_VERBOSITY=error` to your `.env`
- FAISS vector store is **in-memory** — re-upload the document after restarting the app
