"""
Retriever for AI Risk Advisor using Azure AI Search (Hybrid + Vector)

Run:
    python -m app.rag.retriever
"""

import os
from dotenv import load_dotenv

from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from app.security.keyvault import get_secret


def get_query_embedding(client: AzureOpenAI, query: str):
    response = client.embeddings.create(
        model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        input=query,
    )
    return response.data[0].embedding


def search(query: str):
    load_dotenv(override=True)

    openai_api_key = get_secret("AZURE-OPENAI-API-KEY")
    search_admin_key = get_secret("AZURE-SEARCH-ADMIN-KEY")

    openai_client = AzureOpenAI(
        api_key=openai_api_key,
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    search_client = SearchClient(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
        credential=AzureKeyCredential(search_admin_key),
    )

    print(f"\nQuery: {query}")

    query_vector = get_query_embedding(openai_client, query)

    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=5,
        fields="content_vector",
    )

    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query],
        top=5,
    )

    print("\nTop results:\n")

    retrieved = []

    for i, result in enumerate(results, start=1):
        item = {
            "source": result["source"],
            "page_number": result["page_number"],
            "content": result["content"],
        }

        retrieved.append(item)

        print(f"Result {i}:")
        print(f"Source: {item['source']} (Page {item['page_number']})")
        print(item["content"][:300])
        print("-" * 50)

    return retrieved


if __name__ == "__main__":
    search("What does NIST say about AI risk governance?")