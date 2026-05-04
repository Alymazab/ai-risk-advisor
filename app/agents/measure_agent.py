"""
MEASURE Agent for AI Risk Advisor.

Run:
    python -m app.agents.measure_agent
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from app.rag.retriever import search
from app.security.keyvault import get_secret

def run_measure_agent(question: str) -> str:
    load_dotenv()

    client = AzureOpenAI(
        api_key=get_secret("AZURE-OPENAI-API-KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    measure_query = (
        "NIST AI RMF MEASURE function metrics testing evaluation monitoring "
        f"validation performance trustworthiness: {question}"
    )

    results = search(measure_query)

    context = "\n\n---\n\n".join(
        f"Source: {r['source']}, Page: {r['page_number']}\n{r['content']}"
        for r in results
    )

    prompt = f"""
You are the MEASURE specialist agent in an AI Risk Advisor system.

Analyze the user's question only from the NIST AI RMF MEASURE perspective.

Focus on:
- metrics
- testing
- evaluation
- validation
- monitoring
- performance
- trustworthiness
- uncertainty
- measurement limits

Use ONLY the provided NIST context.

User question:
{question}

NIST context:
{context}

Return your answer in this format:

## MEASURE Analysis
Explain what should be measured or evaluated.

## Recommended Metrics / Tests
- Test or metric 1
- Test or metric 2
- Test or metric 3

## Measurement Concerns
- Concern 1
- Concern 2
- Concern 3

## Sources
List source document and page numbers.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": "You are a careful NIST AI RMF MEASURE specialist. Do not hallucinate.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    answer = run_measure_agent(
        "What should be measured for a customer-facing AI chatbot?"
    )
    print(answer)