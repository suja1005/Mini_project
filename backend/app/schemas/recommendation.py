from pydantic import BaseModel
from typing import List, Dict, Optional

class CareerFitItem(BaseModel):
    id: str
    title: str
    category: str
    description: str
    fit_score: int
    why_recommended: List[str]
    needs_improvement: List[str]
    learning_difficulty: str

class RecommendationResponse(BaseModel):
    user_id: str
    top_recommendations: List[CareerFitItem]
    generated_at: str
