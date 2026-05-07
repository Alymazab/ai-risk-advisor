"""
LLM-based risk scoring agent for AI Risk Advisor.
"""

import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

from app.security.keyvault import get_secret


def score_report_with_llm(question: str, report: str) -> dict:
    load_dotenv(override=True)

    client = AzureOpenAI(
        api_key=get_secret("AZURE-OPENAI-API-KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    prompt = f"""
You are an AI risk scoring agent.

Score the AI system based on the user scenario and generated advisory report.

User scenario:
{question}

Advisory report:
{report}

Return ONLY valid JSON. No markdown. No explanation outside JSON.

Use this exact JSON structure:

{{
  "overall_risk_level": "Low | Medium | High | Critical",
  "overall_score": 0,
  "likelihood_score": 0,
  "impact_score": 0,
  "govern_score": 0,
  "map_score": 0,
  "measure_score": 0,
  "manage_score": 0,
  "top_risk_categories": [
    "category 1",
    "category 2",
    "category 3"
  ],
  "scoring_rationale": "Short explanation of why this score was assigned.",
  "executive_decision": "Proceed | Proceed with controls | Redesign required | Pause deployment"
}}

Rules:
- Scores must be integers from 0 to 100.
- Use Critical only when both likelihood and impact are very high.
- Financial, healthcare, hiring, public-facing, regulated, or safety-sensitive systems should generally have higher impact.
- Be realistic, not alarmist.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": "You are a precise AI risk scoring agent. Return valid JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    raw = response.choices[0].message.content.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "overall_risk_level": "Unknown",
            "overall_score": 0,
            "likelihood_score": 0,
            "impact_score": 0,
            "govern_score": 0,
            "map_score": 0,
            "measure_score": 0,
            "manage_score": 0,
            "top_risk_categories": [],
            "scoring_rationale": "Risk scoring failed because the model did not return valid JSON.",
            "executive_decision": "Review required",
            "raw_response": raw,
        }
