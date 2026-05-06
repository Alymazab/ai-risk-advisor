"""
Govern Agent for AI Risk Advisor.

This agent focuses on the GOVERN function of the NIST AI RMF:
- accountability
- policies
- oversight
- roles and responsibilities
- organizational risk culture

Run:
    python -m app.agents.govern_agent
"""

import os
from dotenv import load_dotenv

from openai import AzureOpenAI
from app.rag.retriever import search
from app.security.keyvault import get_secret

def run_govern_agent(question: str) -> str:
    load_dotenv(override=True)

    client = AzureOpenAI(
        api_key=get_secret("AZURE-OPENAI-API-KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    govern_query = f"NIST AI RMF GOVERN function governance accountability oversight policies roles responsibilities: {question}"

    results = search(govern_query)

    context_blocks = []

    for result in results:
        context_blocks.append(
            f"Source: {result['source']}, Page: {result['page_number']}\n"
            f"{result['content']}"
        )

    context = "\n\n---\n\n".join(context_blocks)

    prompt = f"""
You are the GOVERN specialist agent in an AI Risk Advisor system.

Your job is to analyze the user's question only from the NIST AI RMF GOVERN perspective.

Focus on:
- accountability
- governance structure
- policies
- oversight
- roles and responsibilities
- organizational risk culture
- monitoring and review

Use ONLY the provided context.

User question:
{question}

NIST context:
{context}

Return your answer in this format:

## GOVERN Analysis
Explain the governance-related risk considerations.

## Recommended Governance Actions
- Action 1
- Action 2
- Action 3

## Sources
List source document and page numbers.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": "You are a careful NIST AI RMF GOVERN specialist. Do not hallucinate.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    answer = run_govern_agent(
        "What governance controls should be in place for a customer-facing AI chatbot?"
    )
    print(answer)