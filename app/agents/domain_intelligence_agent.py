"""
Domain Intelligence Agent for AI Risk Advisor.

Detects the industry/domain and adds industry-specific regulations,
risks, attack paths, controls, and business consequences.
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

from app.security.keyvault import get_secret


def run_domain_intelligence_agent(question: str) -> str:
    load_dotenv(override=True)

    client = AzureOpenAI(
        api_key=get_secret("AZURE-OPENAI-API-KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    prompt = f"""
You are a senior domain-specific AI risk intelligence analyst.

Your job is to identify the industry/domain of the AI deployment scenario
and produce domain-specific AI risk intelligence.

Do NOT be generic.
Do NOT mix multiple industries unless the user scenario clearly includes multiple industries.
Focus only on the user's scenario.

User scenario:
{question}

Return your answer in this exact format:

## Domain Intelligence

### Detected Domain
State the primary domain. Examples:
- Financial Services
- Healthcare
- Defense / Aerospace
- Government
- Insurance
- Manufacturing
- Legal
- Education
- Enterprise SaaS

### Domain-Specific Sensitive Assets
List the sensitive assets that matter in this domain.

### Domain-Specific Regulatory / Compliance Considerations
List relevant compliance areas.
Examples:
- Finance: GLBA, PCI-DSS, SOX, AML, investment suitability, consumer protection
- Healthcare: HIPAA, PHI, clinical safety, medical liability
- Defense: ITAR, CMMC, NIST 800-171, export-controlled technical data, mission readiness
- Government: public records, procurement, citizen data, service continuity

### Domain-Specific Failure Scenarios
Create 5 realistic domain-specific failure scenarios.
Each must include:
- Failure scenario
- Why it matters in this domain
- Likely consequence
- Required control

### Domain-Specific Attack / Misuse Patterns
Create 5 realistic attack or misuse patterns specific to this domain.

### Domain-Specific Controls
Create a markdown table:

| Control | Domain Relevance | Implementation Detail | Owner | Priority |

Include at least 8 controls.

### Domain Intelligence Summary
Write a short paragraph explaining how the domain changes the risk posture.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a domain-specific AI risk intelligence analyst. "
                    "Be concrete, industry-specific, and avoid generic AI risk language."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    result = run_domain_intelligence_agent(
        "Assess the AI risks of deploying a multimodal generative AI platform for a global defense contractor that processes classified engineering documents, analyzes satellite imagery, generates technical maintenance procedures, and assists employees through an internal AI copilot."
    )
    print(result)