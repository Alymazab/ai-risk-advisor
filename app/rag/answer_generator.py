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

Answer ONLY using the context below.
If unsure, say you don't know.

Question:
{question}

Context:
{context}
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