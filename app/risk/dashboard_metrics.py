def build_dashboard_metrics(risk_score: dict, function_scores: dict) -> dict:
    overall_score = risk_score.get("overall_score", 0)
    likelihood = risk_score.get("likelihood_score", 0)
    impact = risk_score.get("impact_score", 0)

    category_distribution = [
        {"name": "Security", "value": 35},
        {"name": "Compliance", "value": 25},
        {"name": "Operational", "value": 20},
        {"name": "Governance", "value": 15},
        {"name": "Privacy", "value": 5},
    ]

    top_risks = [
        {"rank": 1, "risk": "Data Breach", "score": min(100, overall_score + 12)},
        {"rank": 2, "risk": "Prompt Injection", "score": min(100, overall_score + 8)},
        {"rank": 3, "risk": "Insider Threat", "score": min(100, overall_score + 5)},
        {"rank": 4, "risk": "API Abuse", "score": max(0, overall_score - 2)},
        {"rank": 5, "risk": "Hallucination", "score": max(0, overall_score - 8)},
    ]

    maturity_scores = [
        {"name": "GOVERN", "score": function_scores.get("GOVERN", 0)},
        {"name": "MAP", "score": function_scores.get("MAP", 0)},
        {"name": "MEASURE", "score": function_scores.get("MEASURE", 0)},
        {"name": "MANAGE", "score": function_scores.get("MANAGE", 0)},
    ]

    return {
        "overall_score": overall_score,
        "likelihood": likelihood,
        "impact": impact,
        "risk_level": risk_score.get("overall_risk_level", "Unknown"),
        "executive_decision": risk_score.get("executive_decision", "Review required"),
        "category_distribution": category_distribution,
        "top_risks": top_risks,
        "maturity_scores": maturity_scores,
    }