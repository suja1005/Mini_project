from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PracticalQuestionResponse(BaseModel):
    question_id: str
    skill: str
    topic: str
    difficulty: str
    type: str
    question: str
    options: List[str] = Field(default_factory=list)


class PracticalAssessmentResponse(BaseModel):
    assessment_id: str
    career_title: str
    time_limit_minutes: int
    total_questions: int
    skills: List[str]
    questions: List[PracticalQuestionResponse]


class PracticalAssessmentSubmission(BaseModel):
    assessment_id: str
    answers: Dict[str, Any]


class PracticalSkillResult(BaseModel):
    skill: str
    score: int
    category: str
    correct_count: int
    total_questions: int
    verified: bool


class PracticalAssessmentResult(BaseModel):
    attempt_id: str
    career_title: str
    overall_score: int
    total_questions: int
    correct_count: int
    skill_results: List[PracticalSkillResult]
    claimed_skills: List[str]
    evidence_submitted: Dict[str, int]
    verified_skills: List[str]
    skills_needing_improvement: List[str]
    adaptive_roadmap: List[Dict[str, Any]]
    submitted_at: str


class PracticalAssessmentStatus(BaseModel):
    has_completed: bool
    career_title: str
    skill_results: List[PracticalSkillResult] = Field(default_factory=list)
    claimed_skills: List[str] = Field(default_factory=list)
    evidence_submitted: Dict[str, int] = Field(default_factory=dict)
    verified_skills: List[str] = Field(default_factory=list)
    skills_needing_improvement: List[str] = Field(default_factory=list)
    adaptive_roadmap: List[Dict[str, Any]] = Field(default_factory=list)


class PracticalAssessmentHistoryItem(BaseModel):
    attempt_id: str
    career_title: str
    overall_score: int
    total_questions: int
    correct_count: int
    skill_results: List[PracticalSkillResult]
    submitted_at: str
