from pydantic import BaseModel
from typing import Dict, List, Optional


class AnalyzeRequest(BaseModel):
    scenario: str


class AnalyzeResponse(BaseModel):
    report: str
    risk_score: Dict
    function_scores: Dict
    live_demo_note: Optional[str] = None