from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class QuestionSchema(BaseModel):
    id: Optional[Any] = None
    question_id: Optional[str] = None
    question_number: Optional[int] = None
    category: Optional[str] = None
    skill: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    type: Optional[str] = "mcq"
    question: str
    options: List[str] = []
    # Do NOT expose correct_answer to client!

class AssessmentSubmit(BaseModel):
    answers: Dict[str, Any]  # {"q_id": "Option A" or option index}

class AssessmentReviewItem(BaseModel):
    question_id: str
    question_number: Optional[int] = None
    question: str
    type: Optional[str] = "mcq"
    topic: Optional[str] = None
    user_answer: str
    correct_answer: str
    is_correct: bool
    explanation: Optional[str] = None

class AssessmentResultResponse(BaseModel):
    user_id: str
    overall_score: int
    score: Optional[int] = None
    percentage: Optional[int] = None
    logical_score: Optional[int] = 75
    numerical_score: Optional[int] = 75
    technical_score: Optional[int] = 75
    total_questions: int
    correct_count: int
    passed: Optional[bool] = None
    is_completed: bool = True
    topic_performance: Optional[Dict[str, Any]] = None
    strengths: Optional[List[str]] = None
    weak_topics: Optional[List[Any]] = None
    recommended_revisions: Optional[List[Any]] = None
    reviews: Optional[List[AssessmentReviewItem]] = None
