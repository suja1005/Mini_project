from pydantic import BaseModel
from typing import List, Dict, Optional

class SkillGapItem(BaseModel):
    skill: str
    current: int
    required: int
    gap: int
    priority: str  # HIGH, MEDIUM, LOW

class CareerAnalysisResponse(BaseModel):
    career_id: str
    title: str
    category: str
    fit_score: int
    current_employability: int
    required_employability: int
    employability_gap: int
    learning_effort: str  # LOW, MEDIUM, HIGH
    career_risk: str      # LOW, MEDIUM, HIGH
    achievability: int    # 0-100
    skill_gaps: List[SkillGapItem]
    disclaimer: str = "Model-based estimate. Calculated deterministically from student profile matching algorithms."
