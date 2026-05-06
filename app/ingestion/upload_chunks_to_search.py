"""
Upload NIST AI RMF chunks into Azure AI Search with Azure OpenAI embeddings.

Run from project root:
    python -m app.ingestion.upload_chunks_to_search
"""

import os
from dotenv import load_dotenv

from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import chunk_pages
from pathlib import Path

PDF_PATH = "data/raw/nist_ai_rmf.pdf"


def get_embedding(client: AzureOpenAI, text: str) -> list[float]:
    response = client.embeddings.create(
        model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        input=text,
    )
    return response.data[0].embedding


def upload_chunks() -> None:
    load_dotenv()

    azure_openai_client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
    )

    search_client = SearchClient(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
        credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_ADMIN_KEY")),
    )

    print("Loading PDF...")
    pages = load_pdf(PDF_PATH)

    print("Creating chunks...")
    chunks = chunk_pages(pages)
    print(f"Chunks created: {len(chunks)}")

    documents = []

    print("Creating embeddings and preparing documents...")

    for i, chunk in enumerate(chunks):
        embedding = get_embedding(azure_openai_client, chunk["text"])

        documents.append(
            {
                "id": str(i),
                "content": chunk["text"],
                "content_vector": embedding,
                "source": Path(chunk["metadata"]["source"]).name,
                "page_number": chunk["metadata"]["page_number"],
                "chunk_id": chunk["chunk_id"],
            }
        )

        print(f"Prepared chunk {i + 1}/{len(chunks)}")

    print("Uploading documents to Azure AI Search...")
    result = search_client.upload_documents(documents=documents)

    succeeded = sum(1 for r in result if r.succeeded)
    print(f"Uploaded {succeeded}/{len(documents)} documents.")


if __name__ == "__main__":
    upload_chunks()