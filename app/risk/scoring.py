def calculate_risk_scores(report_text: str):
    text = report_text.lower()

    scores = {
        "governance": 0,
        "privacy": 0,
        "security": 0,
        "bias": 0,
        "reliability": 0,
        "compliance": 0,
    }

    keywords = {
        "governance": ["lack of oversight", "no policy", "unclear accountability"],
        "privacy": ["personal data", "pii", "privacy risk"],
        "security": ["attack", "prompt injection", "abuse"],
        "bias": ["bias", "fairness", "discrimination"],
        "reliability": ["hallucination", "inaccurate", "unreliable"],
        "compliance": ["regulation", "legal", "compliance"],
    }

    for category, words in keywords.items():
        for word in words:
            if word in text:
                scores[category] += 2

    overall = sum(scores.values())

    if overall >= 8:
        level = "High"
    elif overall >= 4:
        level = "Medium"
    else:
        level = "Low"

    return scores, level