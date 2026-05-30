"""
Threat Model Intelligence Agent for AI Risk Advisor.

Adds scenario-specific failure chains, misuse paths, attack paths,
sensitive asset exposure, and enterprise security reasoning.
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

from app.security.keyvault import get_secret


def run_threat_model_agent(question: str, report_context: str) -> str:
    load_dotenv(override=True)

    client = AzureOpenAI(
        api_key=get_secret("AZURE-OPENAI-API-KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    prompt = f"""
You are a senior AI security architect and threat-modeling specialist.

Your job is to analyze the AI deployment scenario and produce realistic,
scenario-specific threat intelligence.

Do NOT write generic AI safety language.
Think like:
- AI red teamer
- enterprise security architect
- cloud security engineer
- AI governance lead
- incident response planner

Before generating attack paths:

1. Determine the industry.
2. Determine the sensitive assets.
3. Determine the AI capabilities.
4. Determine the external integrations.
5. Determine likely adversaries.
6. Build attack chains specific to those findings.

Attack paths must reference:
- assets
- systems
- workflows
- business consequences

Avoid generic examples.

User scenario:
{question}

Existing report context:
{report_context}

Return your answer in this exact format:

## Threat Model Intelligence

### Critical Assets at Risk
Identify the most sensitive assets this AI system could expose, corrupt, misuse, or influence.

### Primary Threat Actors
List realistic threat actors for this scenario:
- external attacker
- malicious insider
- careless employee
- third-party vendor
- compromised integration
- authorized user abusing access

### Realistic Attack Paths
Create 5 realistic attack paths.

Use this format:

#### Attack Path 1: Short Name
- Entry Point:
- Exploitation Method:
- Failure Chain:
- Business Impact:
- Detection Method:
- Recommended Controls:

### AI-Specific Failure Modes
Explain realistic AI-specific failures:
- hallucination
- prompt injection
- data leakage
- tool/API abuse
- model overreliance
- poisoned inputs
- unsafe automation
- sensitive document exposure

### Enterprise Security Controls
Create a markdown table:

| Control | Purpose | Detection Signal | Owner | Priority |

Include at least 8 controls.

### Residual Risk Warning
Write a direct warning explaining what risk remains even after controls are implemented.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a former cloud security architect, AI red team specialist, defense-industry risk consultant, and threat intelligence analyst. "
                    """You must identify:
                    - domain-specific attack paths
                    - operational failure chains
                    - AI misuse scenarios
                    - business consequences
                    - regulatory consequences
                    - realistic adversary behavior"""
                    "Avoid generic cybersecurity advice."
                    "Every finding must be specific to the scenario."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    result = run_threat_model_agent(
        "Assess the AI risks of deploying a multimodal generative AI platform for a defense contractor.",
        "Existing report context.",
    )
    print(result)