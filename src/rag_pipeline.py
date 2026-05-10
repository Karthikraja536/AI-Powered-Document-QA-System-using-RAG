"""
rag_pipeline.py
---------------
Core RAG pipeline using Groq LLM + HuggingFace Embeddings + FAISS vector store.
All settings are imported from config.py.
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import (
    CHUNK_OVERLAP,
    CHUNK_SEPARATORS,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
    GROQ_API_KEY,
    MAX_TOKENS,
    MODEL_NAME,
    PROMPT_TEMPLATE,
    TEMPERATURE,
    TOP_K,
)


class RAGPipeline:
    """
    Retrieval-Augmented Generation pipeline.

    Usage:
        pipeline = RAGPipeline()
        pipeline.ingest("your document text here...")
        result = pipeline.ask("What is the waterfall model?")
        print(result["answer"])
    """

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not found. Please add it to your .env file."
            )

        self.qa_chain = None
        self.retriever = None
        self.num_chunks = 0

        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

        self.llm = ChatGroq(
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            groq_api_key=GROQ_API_KEY,
        )

        self.prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["context", "question"],
        )

    def ingest(self, text: str) -> None:
        """
        Chunks raw text, embeds it, and stores it in a FAISS vector store.

        Args:
            text: Plain text content of the document.
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=CHUNK_SEPARATORS,
        )
        chunks = splitter.split_text(text)
        self.num_chunks = len(chunks)

        vectorstore = FAISS.from_texts(chunks, self.embeddings)
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})

        self.qa_chain = (
            {
                "context": self.retriever | self._format_docs,
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question: str) -> dict:
        """
        Retrieves relevant chunks and generates an answer.

        Args:
            question: User's question about the document.

        Returns:
            Dict with 'answer' (str) and 'sources' (list of str chunks).
        """
        if not self.qa_chain:
            return {
                "answer": "No document loaded. Please upload a file first.",
                "sources": [],
            }

        answer = self.qa_chain.invoke(question)
        source_docs = self.retriever.invoke(question)
        sources = [doc.page_content for doc in source_docs]

        return {"answer": answer, "sources": sources}

    @staticmethod
    def _format_docs(docs) -> str:
        """Joins retrieved document chunks into a single context string."""
        return "\n\n".join(doc.page_content for doc in docs)
