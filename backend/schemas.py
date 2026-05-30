from typing import Dict, Optional
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    scenario: str


class AnalyzeResponse(BaseModel):
    report: str
    risk_score: Dict
    function_scores: Dict
    dashboard_metrics: Dict
    live_demo_note: Optional[str] = None