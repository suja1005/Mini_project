from pydantic import BaseModel
from typing import List, Dict, Optional

class QuestionSchema(BaseModel):
    id: int
    category: str  # Logical Reasoning, Numerical Ability, Technical Aptitude
    question: str
    options: List[str]
    correct_answer: int

class AssessmentSubmit(BaseModel):
    answers: Dict[str, int]  # {"1": 0, "2": 1, ...}

class AssessmentResultResponse(BaseModel):
    user_id: str
    overall_score: int
    logical_score: int
    numerical_score: int
    technical_score: int
    total_questions: int
    correct_count: int
    is_completed: bool = True
