import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Document Q&A",
    page_icon="📄",
    layout="wide"
)

import pdfplumber
import docx2txt
import tempfile
from rag_pipeline import RAGPipeline


# Extract text from uploaded file
def extract_text(uploaded_file):
    file_ext = Path(uploaded_file.name).suffix.lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        if file_ext == ".pdf":
            text = ""
            with pdfplumber.open(tmp_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text

        elif file_ext in [".docx", ".doc"]:
            return docx2txt.process(tmp_path)

        elif file_ext == ".txt":
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        else:
            return None
    finally:
        os.unlink(tmp_path)


# --- UI ---
st.title("📄 Document Q&A Assistant")
st.markdown("Upload a document and ask questions about its content.")

# Initialize session state
if "rag" not in st.session_state:
    st.session_state.rag = RAGPipeline()
if "document_name" not in st.session_state:
    st.session_state.document_name = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "doc_ready" not in st.session_state:
    st.session_state.doc_ready = False

# Sidebar
with st.sidebar:
    st.header("📁 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "doc", "txt"],
        help="Supported formats: PDF, DOCX, DOC, TXT"
    )

    if uploaded_file:
        if uploaded_file.name != st.session_state.document_name:
            with st.spinner("Extracting and indexing document..."):
                text = extract_text(uploaded_file)
                if text and text.strip():
                    st.session_state.rag.ingest(text)
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.chat_history = []
                    st.session_state.doc_ready = True
                    st.success(f"✅ Loaded: {uploaded_file.name}")
                    st.info(f"📊 {st.session_state.rag.num_chunks} chunks indexed")
                else:
                    st.error("Could not extract text from this file.")

    if st.session_state.document_name:
        st.markdown("---")
        st.markdown(f"**Current document:**  \n{st.session_state.document_name}")
        if st.button("🗑️ Clear Document"):
            st.session_state.rag = RAGPipeline()
            st.session_state.document_name = None
            st.session_state.chat_history = []
            st.session_state.doc_ready = False
            st.rerun()

# Main chat area
if st.session_state.doc_ready:
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask a question about your document...")

    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching document and thinking..."):
                try:
                    result = st.session_state.rag.ask(question)
                    answer = result["answer"]
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

else:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        ### 👈 Get Started

        1. **Upload** a PDF, DOCX, or TXT file from the sidebar
        2. **Wait** for the document to be chunked and indexed
        3. **Ask** any question about your document

        The AI will search the most relevant parts and answer accurately.
        """)
