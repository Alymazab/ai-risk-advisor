"""
Create Azure AI Search index for AI Risk Advisor.

Run from project root:
    python -m app.ingestion.create_search_index
"""

import os
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)


def create_index() -> None:
    load_dotenv()

    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_SEARCH_ADMIN_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "ai-risk-advisor-index")

    if not endpoint or not key:
        raise ValueError("Missing AZURE_SEARCH_ENDPOINT or AZURE_SEARCH_ADMIN_KEY")

    client = SearchIndexClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="source", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="page_number", type=SearchFieldDataType.Int32, filterable=True),
        SimpleField(name="chunk_id", type=SearchFieldDataType.String, filterable=True),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="ai-risk-vector-profile",
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(name="ai-risk-hnsw")
        ],
        profiles=[
            VectorSearchProfile(
                name="ai-risk-vector-profile",
                algorithm_configuration_name="ai-risk-hnsw",
            )
        ],
    )

    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search,
    )

    client.create_or_update_index(index)

    print(f"Created or updated index: {index_name}")


if __name__ == "__main__":
    create_index()