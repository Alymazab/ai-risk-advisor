"""
NIST AI RMF Playbook Agent.

Retrieves richer implementation guidance from the public NIST AI RMF Playbook
function pages: GOVERN, MAP, MEASURE, MANAGE.

Run:
    python -m app.agents.playbook_agent
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import AzureOpenAI

from app.security.keyvault import get_secret


PLAYBOOK_URLS = {
    "GOVERN": "https://airc.nist.gov/airmf-resources/playbook/govern/",
    "MAP": "https://airc.nist.gov/airmf-resources/playbook/map/",
    "MEASURE": "https://airc.nist.gov/airmf-resources/playbook/measure/",
    "MANAGE": "https://airc.nist.gov/airmf-resources/playbook/manage/",
}


def fetch_page_text(url: str) -> str:
    headers = {"User-Agent": "AI-Risk-Advisor/1.0"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def collect_relevant_blocks(text: str, question: str, function_name: str, max_chars: int = 9000) -> str:
    """
    Pull richer blocks from the Playbook page.
    This favors suggested actions, about sections, questions, references to monitoring,
    documentation, accountability, testing, impact, and risk management.
    """

    scenario_terms = [
        word.lower()
        for word in re.findall(r"[A-Za-z]{4,}", question)
        if len(word) > 3
    ]

    priority_terms = [
        function_name.lower(),
        "suggested actions",
        "about",
        "risk",
        "accountability",
        "documentation",
        "monitoring",
        "audit",
        "oversight",
        "impact",
        "stakeholder",
        "privacy",
        "security",
        "bias",
        "fairness",
        "validation",
        "testing",
        "measurement",
        "incident",
        "third-party",
        "governance",
        "compliance",
        "human oversight",
        "data quality",
        "transparency",
        "explainability",
        "decommissioning",
        "feedback",
        "redress",
        "recourse",
    ]

    blocks = text.split("\n\n")
    scored_blocks = []

    for block in blocks:
        clean = block.strip()
        if len(clean) < 80:
            continue

        lower = clean.lower()
        score = 0

        for term in priority_terms:
            if term in lower:
                score += 3

        for term in scenario_terms:
            if term in lower:
                score += 1

        if "suggested actions" in lower:
            score += 8

        if "establish" in lower or "document" in lower or "identify" in lower:
            score += 2

        if score > 0:
            scored_blocks.append((score, clean))

    scored_blocks.sort(key=lambda x: x[0], reverse=True)

    selected = []
    current_len = 0

    for _, block in scored_blocks:
        if current_len + len(block) > max_chars:
            continue

        selected.append(block)
        current_len += len(block)

        if current_len >= max_chars:
            break

    if not selected:
        return text[:max_chars]

    return "\n\n---\n\n".join(selected)


def fetch_playbook_context(question: str) -> tuple[str, str]:
    contexts = []
    source_lines = []

    for function_name, url in PLAYBOOK_URLS.items():
        try:
            page_text = fetch_page_text(url)
            relevant = collect_relevant_blocks(page_text, question, function_name)
            contexts.append(
                f"## {function_name} PLAYBOOK SOURCE\nURL: {url}\n\n{relevant}"
            )
            source_lines.append(f"- {function_name}: {url}")
        except Exception as exc:
            contexts.append(
                f"## {function_name} PLAYBOOK SOURCE\nURL: {url}\n\nRetrieval failed: {exc}"
            )
            source_lines.append(f"- {function_name}: {url} (retrieval failed)")

    return "\n\n====================\n\n".join(contexts), "\n".join(source_lines)


def run_playbook_agent(question: str, report_context: str) -> str:
    load_dotenv(override=True)

    client = AzureOpenAI(
        api_key=get_secret("AZURE-OPENAI-API-KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    playbook_context, playbook_sources = fetch_playbook_context(question)

    prompt = f"""
You are the NIST AI RMF Playbook Implementation Agent.

Your job is to enrich the AI Risk Advisory Report with detailed implementation guidance
from the NIST AI RMF Playbook.

Use ONLY the provided Playbook context.
Do not invent page numbers.
Do not claim the Playbook is a legal requirement.
Do not treat the Playbook as a checklist.
Make the guidance specific to the user's AI scenario.
Be concrete, operational, and detailed.

User scenario:
{question}

Existing AI risk report context:
{report_context}

Retrieved NIST AI RMF Playbook sources:
{playbook_sources}

Retrieved NIST AI RMF Playbook context:
{playbook_context}

Return your answer in this exact format:

## NIST AI RMF Playbook Implementation Guidance

### Playbook Retrieval Summary
Briefly explain that guidance was retrieved from the NIST AI RMF Playbook function pages for GOVERN, MAP, MEASURE, and MANAGE.

### Most Relevant Playbook Themes
- Theme 1
- Theme 2
- Theme 3
- Theme 4
- Theme 5
- Theme 6

### GOVERN Implementation Guidance
Provide 5-7 practical governance actions. Include accountability, policy, oversight, documentation, escalation, and human-AI role clarity.

### MAP Implementation Guidance
Provide 5-7 practical mapping actions. Include system context, intended use, stakeholders, impacted groups, data dependencies, third-party dependencies, and foreseeable misuse.

### MEASURE Implementation Guidance
Provide 5-7 practical measurement actions. Include testing, validation, performance, bias/fairness, privacy/security testing, monitoring, and uncertainty limits.

### MANAGE Implementation Guidance
Provide 5-7 practical management actions. Include risk prioritization, mitigation, approval gates, incident response, residual risk, feedback loops, and decommissioning triggers.

### Playbook-Informed Control Enhancements
Create a detailed markdown table with these columns:
| NIST Function | Control Area | Playbook-Informed Enhancement | Why It Matters | Implementation Owner |

Include at least 10 rows.

### Playbook-Informed Questions for Leadership
Create 8 strong questions executives should answer before deployment.

### Playbook Sources
Use these source URLs:
{playbook_sources}
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful NIST AI RMF Playbook implementation specialist. "
                    "Use only the retrieved Playbook context and do not invent sources."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    answer = run_playbook_agent(
        "Assess the AI risks of deploying a customer-facing AI chatbot for a financial services company.",
        "Finance chatbot risk report context.",
    )
    print(answer)