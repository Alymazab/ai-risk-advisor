"""
MAP Agent for AI Risk Advisor.

This agent focuses on the MAP function of the NIST AI RMF:
- context
- intended use
- stakeholders
- impacts
- risk sources
- system boundaries

Run:
    python -m app.agents.map_agent
"""

import os
from dotenv import load_dotenv

from openai import AzureOpenAI
from app.rag.retriever import search
from app.security.keyvault import get_secret

def run_map_agent(question: str) -> str:
    load_dotenv(override=True)

    client = AzureOpenAI(
        api_key=get_secret("AZURE-OPENAI-API-KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    map_query = (
        "NIST AI RMF MAP function context intended use stakeholders impacts "
        f"risk sources system boundaries: {question}"
    )

    results = search(map_query)

    context_blocks = []

    for result in results:
        context_blocks.append(
            f"Source: {result['source']}, Page: {result['page_number']}\n"
            f"{result['content']}"
        )

    context = "\n\n---\n\n".join(context_blocks)

    prompt = f"""
You are the MAP specialist agent in an AI Risk Advisor system.

Your job is to analyze the user's question only from the NIST AI RMF MAP perspective.

Focus on:
- intended use
- system context
- stakeholders
- affected individuals and groups
- benefits and harms
- risk sources
- system boundaries
- assumptions and dependencies

Use ONLY the provided context.

User question:
{question}

NIST context:
{context}

Return your answer in this format:

## MAP Analysis
Explain the context, stakeholders, intended use, and risk sources.

## Key Mapping Questions
- Question 1
- Question 2
- Question 3

## Recommended MAP Actions
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
                "content": "You are a careful NIST AI RMF MAP specialist. Do not hallucinate.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    answer = run_map_agent(
        "What risks should be mapped for a customer-facing AI chatbot?"
    )
    print(answer)