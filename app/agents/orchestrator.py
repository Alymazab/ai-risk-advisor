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
from app.agents.playbook_agent import run_playbook_agent

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
    load_dotenv(override=True)

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
    print("Running NIST Playbook agent...")
    playbook_output = run_playbook_agent(
        question,
        "\n\n".join([govern_output, map_output, measure_output, manage_output]),
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
Important: The NIST Playbook section must be detailed and operational. Do not compress it into generic bullets.
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

NIST AI RMF Playbook agent output:
{playbook_output}

Verified source pages extracted programmatically:
{verified_sources}

Return your final answer in this exact format:

# AI Risk Advisory Report

## Executive Summary
Write a polished 5-7 sentence executive summary. Include the overall risk posture, business impact, and why this AI use case requires governance.

## Scenario Classification
- Industry / Domain:
- AI System Type:
- Primary Users:
- Affected Stakeholders:
- Risk Sensitivity:
- Likely Deployment Environment:

## Risk Category Overview
Create a concise overview of the most relevant risk categories for this scenario, such as:
- Governance and accountability
- Privacy and data protection
- Cybersecurity and abuse
- Bias and fairness
- Transparency and explainability
- Reliability and hallucination
- Human oversight
- Monitoring and incident response
- Regulatory / compliance exposure

## GOVERN Findings
Summarize governance risks, accountability gaps, oversight needs, policies, ownership, and review processes.

## MAP Findings
Summarize context, stakeholders, intended use, foreseeable misuse, affected groups, system boundaries, and impact areas.

## MEASURE Findings
Summarize metrics, testing, evaluation, validation, monitoring, and trustworthiness measurement needs.

## MANAGE Findings
Summarize mitigation, prioritization, risk treatment, residual risk handling, escalation, and ongoing improvement.

## Risk Register
Create a markdown table with these columns:
| Risk | Category | Likelihood | Impact | Priority | Recommended Control |

Include 6-8 realistic risks.

## Priority Recommendations
Provide 5 strong recommendations. Each one should be practical and implementation-focused.

## 30-60-90 Day Roadmap
Create a practical roadmap:
- First 30 days:
- Days 31-60:
- Days 61-90:

## NIST Playbook Implementation Guidance
Use the Playbook agent output as the primary source for this section.
Preserve rich implementation detail.
Include:
- Playbook Retrieval Summary
- Most Relevant Playbook Themes
- GOVERN Implementation Guidance
- MAP Implementation Guidance
- MEASURE Implementation Guidance
- MANAGE Implementation Guidance
- Playbook-Informed Control Enhancements table
- Playbook-Informed Questions for Leadership
- Playbook Sources
Do not reduce this section to a short bullet list.

## Executive Decision
State whether the system should proceed, proceed with controls, require redesign, or be paused pending risk treatment.

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