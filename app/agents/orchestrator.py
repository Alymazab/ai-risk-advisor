"""
Orchestrator Agent for AI Risk Advisor.

Runs all four NIST AI RMF specialist agents:
- GOVERN
- MAP
- MEASURE
- MANAGE

Run:
    python -m app.agents.orchestrator
"""

import os
import re
from dotenv import load_dotenv
from openai import AzureOpenAI

from app.agents.govern_agent import run_govern_agent
from app.agents.map_agent import run_map_agent
from app.agents.measure_agent import run_measure_agent
from app.agents.manage_agent import run_manage_agent
from app.security.keyvault import get_secret

def extract_unique_sources(*agent_outputs: str) -> str:
    """
    Extract unique source references from all agent outputs.

    This makes the final Sources section code-controlled instead of
    relying on the LLM to guess or reconstruct source pages.
    """

    sources = set()

    pattern = re.compile(
        r"nist_ai_rmf\.pdf[, ]+\s*[Pp]age[: ]+\s*(\d+)"
    )

    for output in agent_outputs:
        matches = pattern.findall(output)

        for page_number in matches:
            sources.add(f"nist_ai_rmf.pdf, page {page_number}")

    if not sources:
        return "No explicit source pages found."

    return "\n".join(f"- {source}" for source in sorted(sources))


def run_orchestrator(question: str) -> str:
    load_dotenv()

    print("Running GOVERN agent...")
    govern_output = run_govern_agent(question)

    print("Running MAP agent...")
    map_output = run_map_agent(question)

    print("Running MEASURE agent...")
    measure_output = run_measure_agent(question)

    print("Running MANAGE agent...")
    manage_output = run_manage_agent(question)

    verified_sources = extract_unique_sources(
        govern_output,
        map_output,
        measure_output,
        manage_output,
    )

    client = AzureOpenAI(
        api_key=get_secret("AZURE-OPENAI-API-KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    prompt = f"""
You are the Orchestrator Agent for an AI Risk Advisor system.

You will receive analysis from four specialist agents aligned with the NIST AI RMF:
- GOVERN
- MAP
- MEASURE
- MANAGE

Your job is to synthesize their findings into one clear executive-style advisory report.

User question:
{question}

GOVERN agent output:
{govern_output}

MAP agent output:
{map_output}

MEASURE agent output:
{measure_output}

MANAGE agent output:
{manage_output}

Verified source pages extracted programmatically:
{verified_sources}

Return your final answer in this exact format:

# AI Risk Advisory Report

## Executive Summary
Summarize the overall risk posture in 4-6 sentences.

## GOVERN Findings
Summarize governance risks and controls.

## MAP Findings
Summarize context, stakeholders, impacts, and risk sources.

## MEASURE Findings
Summarize metrics, testing, monitoring, and evaluation needs.

## MANAGE Findings
Summarize mitigation, prioritization, and residual risk handling.

## Priority Recommendations
- Recommendation 1
- Recommendation 2
- Recommendation 3
- Recommendation 4

## Sources
Use ONLY the verified source pages provided above. Do not invent additional sources.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": "You are a careful AI risk orchestration agent. Do not invent unsupported claims or sources.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    report = run_orchestrator(
        "Assess the AI risks of deploying a customer-facing AI chatbot for a financial services company."
    )
    print(report)