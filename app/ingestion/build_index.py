"""
Build FAISS Vector Index for AI Risk Advisor

This script:
1. Loads the NIST AI RMF PDF
2. Splits it into chunks
3. Creates embeddings with OpenAI
4. Saves a FAISS vector database locally

Run from project root:
    python -m app.ingestion.build_index
"""

from pathlib import Path
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import chunk_pages
from app.security.keyvault import get_secret

PDF_PATH = "data/raw/nist_ai_rmf.pdf"
VECTORSTORE_PATH = "data/vectorstore/faiss_index"


def build_faiss_index() -> None:
    load_dotenv()

    print("Loading PDF...")
    pages = load_pdf(PDF_PATH)
    print(f"Loaded pages: {len(pages)}")

    print("Creating chunks...")
    chunks = chunk_pages(pages)
    print(f"Created chunks: {len(chunks)}")

    print("Converting to documents...")
    documents = [
        Document(
            page_content=chunk["text"],
            metadata={
                "chunk_id": chunk["chunk_id"],
                **chunk["metadata"],
            },
        )
        for chunk in chunks
    ]

    print("Creating embeddings...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    print("Building FAISS index...")
    vectorstore = FAISS.from_documents(documents, embeddings)

    output_path = Path(VECTORSTORE_PATH)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Saving index to: {VECTORSTORE_PATH}")
    vectorstore.save_local(VECTORSTORE_PATH)

    print("Done. Vector index created successfully.")


if __name__ == "__main__":
    build_faiss_index()