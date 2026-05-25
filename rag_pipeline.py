"""
rag_pipeline.py
---------------
Core RAG pipeline - using Groq LLM + HuggingFace Embeddings
API key loaded from .env file
"""

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings


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


class RAGPipeline:
    def __init__(self):
        self.qa_chain = None
        self.retriever = None
        self.num_chunks = 0

        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in .env file.")

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0,
            max_tokens=500,
            groq_api_key=groq_api_key
        )

        self.prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )

    def ingest(self, text: str):
        """Takes raw text, chunks it, embeds it, stores in FAISS."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=80,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks = splitter.split_text(text)
        self.num_chunks = len(chunks)

        vectorstore = FAISS.from_texts(chunks, self.embeddings)
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.qa_chain = (
            {
                "context": self.retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question: str) -> dict:
        """Retrieves relevant chunks and generates an answer."""
        if not self.qa_chain:
            return {"answer": "No document loaded. Please upload a file first.", "sources": []}

        answer = self.qa_chain.invoke(question)
        source_docs = self.retriever.invoke(question)
        sources = [doc.page_content for doc in source_docs]
        return {"answer": answer, "sources": sources}
