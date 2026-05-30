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
from app.agents.threat_model_agent import run_threat_model_agent
from app.agents.domain_intelligence_agent import run_domain_intelligence_agent

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

    print("Running Domain Intelligence agent...")
    domain_intelligence_output = run_domain_intelligence_agent(question)

    print("Running NIST Playbook agent...")
    playbook_output = run_playbook_agent(
        question,
        "\n\n".join([govern_output, map_output, measure_output, manage_output]),
    )
    print("Running Threat Model Intelligence agent...")

    threat_model_output = run_threat_model_agent(
        question,
        "\n\n".join([
            govern_output,
            map_output,
            measure_output,
            manage_output,
            playbook_output,
        ]),
    )

    client = AzureOpenAI(
        api_key=get_secret("AZURE-OPENAI-API-KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    prompt = f"""
You are the Orchestrator Agent for an AI Risk Advisor system.

If the Domain Intelligence agent identifies a specific domain, the entire report must stay focused on that domain. Do not introduce unrelated industries or examples.

Important domain rule:
Analyze ONLY the user-provided scenario. Do not combine it with previous examples, default examples, or other industries. If the user scenario is about defense, the report must focus on defense. If it is about finance, the report must focus on finance.

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

Threat Model Intelligence agent output:
{threat_model_output}

Important writing rules:
- Do not write generic AI safety language.
- Be specific to the scenario.
- Write like a senior AI risk consultant.
- Use concrete controls, owners, and evidence.
- Make the report useful for an executive review meeting.
- The final report should feel like a professional consulting deliverable, not a chatbot answer.

Return your final answer in this exact format:

# AI Risk Advisory Report

## Executive Brief
Write this like a board-facing risk memo. Be specific, direct, and opinionated.
Include:
- what the AI system does
- why the risk is material
- what could go wrong operationally, legally, financially, or reputationally
- whether the system should proceed
- the top 3 conditions required before deployment

## Risk Posture Snapshot
Create a concise snapshot:
- Overall Risk:
- Business Criticality:
- Regulatory Exposure:
- Data Sensitivity:
- Automation Impact:
- Human Oversight Requirement:
- Deployment Recommendation:

## Scenario Classification
- Industry / Domain:
- AI System Type:
- Primary Users:
- Affected Stakeholders:
- Data Types Involved:
- External Dependencies:
- Risk Sensitivity:
- Likely Deployment Environment:

## Domain Intelligence
Use the Domain Intelligence agent output as the primary source.
Do not summarize this section into generic bullets.
Preserve:
- Detected Domain
- Domain-Specific Sensitive Assets
- Regulatory / Compliance Considerations
- Failure Scenarios
- Attack / Misuse Patterns
- Domain-Specific Controls
- Domain Intelligence Summary

## Critical Risk Narrative
Write a strong narrative explaining the most serious risk paths.
Do not be generic.
Explain how failures could occur in the real world.
Include adversarial misuse, data leakage, hallucination, automation overreliance, compliance failure, and governance breakdown where relevant.

## Threat Model Intelligence
Use the Threat Model Intelligence agent output as the primary source.
Include:
- Critical Assets at Risk
- Primary Threat Actors
- Realistic Attack Paths
- AI-Specific Failure Modes
- Enterprise Security Controls
- Residual Risk Warning

## Top Enterprise Risks
Create a ranked table:
| Rank | Risk | Why It Matters | Business Impact | Control Priority |

Include 8-10 risks.

## NIST AI RMF Analysis

## Risk Register
Create a detailed markdown table:
| Risk | Category | Likelihood | Impact | Priority | Detection Method | Recommended Control | Owner |

Include 10-12 realistic risks.

## Control Implementation Plan
Create a detailed markdown table:
| Control | NIST Function | Implementation Detail | Evidence Required | Owner | Timeline |
Include at least 10 controls.

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

Do not reduce this section to generic bullets.

## 30-60-90 Day Execution Roadmap
Create a practical roadmap:
- First 30 days:
- Days 31-60:
- Days 61-90:
Each phase should include governance, testing, security, monitoring, and stakeholder actions.

## Executive Decision
Choose one:
- Proceed
- Proceed with controls
- Redesign required
- Pause deployment

Then explain why in 4-6 sentences.

## Sources
Use ONLY the verified source pages provided above and Playbook source URLs.
Do not invent additional sources.

The Threat Model Intelligence section must appear BEFORE Top Enterprise Risks.
Do not place Threat Model Intelligence after Sources.
Sources must always be the final section.
Do not shorten this into generic security bullets.

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