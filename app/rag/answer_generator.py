import os
from dotenv import load_dotenv

from openai import AzureOpenAI
from app.rag.retriever import search


def generate_answer(question: str) -> str:
    load_dotenv()

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    results = search(question)

    context_blocks = []

    for result in results:
        context_blocks.append(
            f"Source: {result['source']}, Page: {result['page_number']}\n"
            f"{result['content']}"
        )

    context = "\n\n---\n\n".join(context_blocks)

    prompt = f"""
You are an AI Risk Advisor using the NIST AI Risk Management Framework.

Answer the user's question using ONLY the provided context.
If the context does not contain enough information, say:
"I do not have enough information from the provided NIST context."

Question:
{question}

Context:
{context}

Return your answer in this exact format:

## Direct Answer
Give a clear answer in 3-5 sentences.

## Key NIST AI RMF Points
- Bullet point 1
- Bullet point 2
- Bullet point 3

## Sources
List the source document and page numbers used.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a careful AI risk advisor. Do not hallucinate."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    answer = generate_answer("What does NIST say about AI risk governance?")
    print(answer)