"""
app.py
------
Streamlit entry point for the Document Q&A Assistant.
UI layer only — all business logic lives in src/.
"""

import streamlit as st

from src.document_loader import extract_text
from src.rag_pipeline import RAGPipeline

# --- Page Config ---
st.set_page_config(
    page_title="Document Q&A",
    page_icon="📄",
    layout="wide",
)


# --- Session State Initialization ---
def init_session_state():
    if "rag" not in st.session_state:
        st.session_state.rag = RAGPipeline()
    if "document_name" not in st.session_state:
        st.session_state.document_name = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "doc_ready" not in st.session_state:
        st.session_state.doc_ready = False


def clear_document():
    st.session_state.rag = RAGPipeline()
    st.session_state.document_name = None
    st.session_state.chat_history = []
    st.session_state.doc_ready = False


# --- Sidebar ---
def render_sidebar():
    with st.sidebar:
        st.header("📁 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "docx", "doc", "txt"],
            help="Supported formats: PDF, DOCX, DOC, TXT",
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
                        st.info(
                            f"📊 {st.session_state.rag.num_chunks} chunks indexed"
                        )
                    else:
                        st.error("Could not extract text from this file.")

        if st.session_state.document_name:
            st.markdown("---")
            st.markdown(
                f"**Current document:**  \n{st.session_state.document_name}"
            )
            if st.button("🗑️ Clear Document"):
                clear_document()
                st.rerun()


# --- Chat Area ---
def render_chat():
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
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as e:
                    st.error(f"Error getting answer: {str(e)}")


# --- Welcome Screen ---
def render_welcome():
    st.markdown("---")
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        ### 👈 Get Started

        1. **Upload** a PDF, DOCX, or TXT file from the sidebar
        2. **Wait** for the document to be chunked and indexed
        3. **Ask** any question about your document

        The AI will search the most relevant parts and answer accurately.
        """)


# --- Main ---
def main():
    init_session_state()
    st.title("📄 Document Q&A Assistant")
    st.markdown("Upload a document and ask questions about its content.")
    render_sidebar()

    if st.session_state.doc_ready:
        render_chat()
    else:
        render_welcome()


if __name__ == "__main__":
    main()