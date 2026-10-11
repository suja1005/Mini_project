from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SubtopicSchema(BaseModel):
    id: str
    title: str
    completed: bool = False

class TopicSchema(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    subtopics: List[SubtopicSchema] = []
    completed: bool = False

class RoadmapResourceSchema(BaseModel):
    title: str
    type: str  # Documentation, Video, Article, Interactive
    url: Optional[str] = None
    provider: Optional[str] = None

class RoadmapTaskSchema(BaseModel):
    id: str
    roadmap_id: str
    phase: int = 1
    phase_name: str = "Phase 1"
    title: str
    description: str
    difficulty: str = "Beginner"  # Beginner, Intermediate, Advanced
    estimated_hours: str = "3 hours"
    priority: str = "HIGH"  # HIGH, MEDIUM, LOW
    status: str = "NOT_STARTED"  # LOCKED, NOT_STARTED, IN_PROGRESS, LEARNING_COMPLETED, VERIFICATION_PENDING, VERIFIED, FAILED
    order: int = 1
    prerequisites: List[str] = []
    skill: str = "General"
    type: str = "Learning"
    explanation: str = ""
    topics: List[TopicSchema] = []
    learning_objectives: List[str] = []
    passing_score: int = 70
    verification_status: str = "Not Started"
    quiz_score: Optional[int] = None
    attempts_count: int = 0
    learning_progress_percentage: int = 0
    resources: List[RoadmapResourceSchema] = []
    completed_at: Optional[str] = None

class RoadmapTaskUpdate(BaseModel):
    status: str

class ToggleSubtopicRequest(BaseModel):
    topic_id: str
    subtopic_id: str
    completed: bool

class RoadmapGenerateRequest(BaseModel):
    career_id: Optional[str] = "ai-engineer"

class RoadmapResponse(BaseModel):
    id: str
    user_id: str
    career_id: str
    career_title: str
    target_employability: int
    current_employability: int
    employability_gap: int
    total_tasks: int
    verified_tasks: int = 0
    completed_tasks: int = 0
    progress_percentage: int = 0
    phases: List[str] = []
    tasks: List[RoadmapTaskSchema] = []
    last_updated: str

class QuizQuestionResponse(BaseModel):
    question_id: str
    question: str
    options: List[str]
    topic: str
    difficulty: str

class QuizSubmissionRequest(BaseModel):
    answers: Dict[str, str]

class QuizResultResponse(BaseModel):
    task_id: str
    score: int
    total_questions: int
    percentage: int
    passed: bool
    status: str
    topic_performance: Dict[str, int]
    weak_topics: List[str]
    message: str
    unlocked_next_task: bool = False
    attempts_count: int = 1

class VerificationAttemptSchema(BaseModel):
    id: str
    task_id: str
    student_id: str
    attempt_number: int
    score: int
    total_questions: int
    percentage: int
    passed: bool
    topic_performance: Dict[str, int]
    created_at: str
