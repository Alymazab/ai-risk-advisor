"""
MANAGE Agent for AI Risk Advisor.

Run:
    python -m app.agents.manage_agent
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from app.rag.retriever import search
from app.security.keyvault import get_secret

def run_manage_agent(question: str) -> str:
    load_dotenv(override=True)

    client = AzureOpenAI(
        api_key=get_secret("AZURE-OPENAI-API-KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    manage_query = (
        "NIST AI RMF MANAGE function risk mitigation treatment response "
        f"prioritization residual risk monitoring improvement: {question}"
    )

    results = search(manage_query)

    context = "\n\n---\n\n".join(
        f"Source: {r['source']}, Page: {r['page_number']}\n{r['content']}"
        for r in results
    )

    prompt = f"""
You are the MANAGE specialist agent in an AI Risk Advisor system.

Analyze the user's question only from the NIST AI RMF MANAGE perspective.

Focus on:
- risk treatment
- risk response
- mitigation
- prioritization
- residual risk
- monitoring improvements
- documenting risk decisions
- reducing unacceptable risk

Use ONLY the provided NIST context.

User question:
{question}

NIST context:
{context}

Return your answer in this format:

## MANAGE Analysis
Explain how the identified AI risks should be managed.

## Recommended Risk Treatments
- Treatment 1
- Treatment 2
- Treatment 3

## Residual Risk Considerations
- Consideration 1
- Consideration 2
- Consideration 3

## Sources
List source document and page numbers.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": "You are a careful NIST AI RMF MANAGE specialist. Do not hallucinate.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    answer = run_manage_agent(
        "How should risks be managed for a customer-facing AI chatbot?"
    )
    print(answer)