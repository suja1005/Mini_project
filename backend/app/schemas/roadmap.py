from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# ============================================================================
# Core Subtopic and Topic Schemas
# ============================================================================

class SubtopicSchema(BaseModel):
    id: str
    title: str
    completed: bool = False

class PracticeTaskSchema(BaseModel):
    id: str
    title: str
    instructions: str
    starter_code: Optional[str] = None
    hint: Optional[str] = None
    completed: bool = False

class RoadmapResourceSchema(BaseModel):
    title: str
    type: str  # Documentation, Video, Article, Interactive
    url: Optional[str] = None
    provider: Optional[str] = None

class LevelTopicSchema(BaseModel):
    id: str
    title: str
    description: str
    estimated_hours: str = "2 hours"
    learning_material: Optional[str] = None
    practical_example: Optional[str] = None
    practice_task: Optional[PracticeTaskSchema] = None
    resources: List[RoadmapResourceSchema] = []
    completed: bool = False
    practice_completed: bool = False
    subtopics: List[SubtopicSchema] = []

class TopicSchema(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    subtopics: List[SubtopicSchema] = []
    completed: bool = False

# ============================================================================
# Level and Skill Schemas
# ============================================================================

class SkillLevelSchema(BaseModel):
    id: str
    skill: str
    skill_slug: str
    level: int  # 1, 2, 3
    level_name: str  # "Level 1 – Beginner", "Level 2 – Intermediate", "Level 3 – Advanced"
    title: str
    description: str
    difficulty: str  # "Beginner", "Intermediate", "Advanced"
    estimated_hours: str
    learning_objectives: List[str] = []
    topics: List[LevelTopicSchema] = []
    prerequisites: List[str] = []
    status: str = "LOCKED"  # LOCKED, AVAILABLE, IN_PROGRESS, ASSESSMENT_PENDING, PASSED, NEEDS_REVISION
    learning_progress_percentage: int = 0
    assessment_status: str = "NOT_STARTED"  # NOT_STARTED, IN_PROGRESS, PASSED, FAILED
    quiz_score: Optional[int] = None
    attempts_count: int = 0
    passing_score: int = 80
    time_limit_minutes: int = 30
    completed_at: Optional[str] = None

class SkillOverviewSchema(BaseModel):
    skill: str
    skill_slug: str
    category: str = "Technical"  # Technical, Foundational, Soft
    description: str
    icon: Optional[str] = None
    total_levels: int = 3
    passed_levels: int = 0
    current_level: int = 1
    progress_percentage: int = 0
    total_learning_hours: str = "60 hours"
    levels: List[SkillLevelSchema] = []

# ============================================================================
# Request Schemas
# ============================================================================

class RoadmapTaskUpdate(BaseModel):
    status: str

class ToggleSubtopicRequest(BaseModel):
    topic_id: str
    subtopic_id: str
    completed: bool

class ToggleLevelTopicRequest(BaseModel):
    completed: Optional[bool] = None
    practice_completed: Optional[bool] = None

class CompleteTopicRequest(BaseModel):
    practice_answer: Optional[str] = None

class RoadmapGenerateRequest(BaseModel):
    career_id: Optional[str] = "ai-engineer"

# ============================================================================
# Legacy / Backward Compatible Task Schema
# ============================================================================

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
    passing_score: int = 80
    verification_status: str = "Not Started"
    quiz_score: Optional[int] = None
    attempts_count: int = 0
    learning_progress_percentage: int = 0
    resources: List[RoadmapResourceSchema] = []
    completed_at: Optional[str] = None

class RoadmapResponse(BaseModel):
    id: Optional[str] = None
    user_id: str
    career_id: str
    career_title: str
    description: Optional[str] = None
    target_employability: Optional[int] = 80
    current_employability: Optional[int] = 50
    employability_gap: Optional[int] = 30
    total_tasks: Optional[int] = 0
    verified_tasks: Optional[int] = 0
    completed_tasks: Optional[int] = 0
    progress_percentage: int = 0
    overall_progress: Optional[int] = 0
    completed_topics_count: Optional[int] = 0
    total_topics_count: Optional[int] = 0
    phases: List[Any] = []
    tasks: Optional[List[RoadmapTaskSchema]] = []
    skills: Optional[List[SkillOverviewSchema]] = []
    completed_topics: Optional[List[Any]] = []
    pending_topics: Optional[List[Any]] = []
    current_learning_topic: Optional[Any] = None
    next_recommended_action: Optional[str] = None
    passing_score_requirement: Optional[int] = 80
    last_updated: Optional[str] = None

# ============================================================================
# Level Assessment Schemas (20 Questions: 15 MCQ + 5 Practical)
# ============================================================================

class AssessmentQuestionClientSchema(BaseModel):
    question_id: str
    question_number: int
    type: str = "mcq"  # "mcq" | "practical"
    question: str
    topic: str
    difficulty: str
    options: List[str] = []
    starter_code: Optional[str] = None
    practical_type: Optional[str] = None

class AssessmentGenerateResponse(BaseModel):
    level_id: str
    skill: str
    level: int
    total_questions: int = 20
    time_limit_minutes: int = 30
    questions: List[AssessmentQuestionClientSchema]

class AssessmentSubmissionRequest(BaseModel):
    answers: Dict[str, str]

class QuestionReviewSchema(BaseModel):
    question_id: str
    question_number: int
    question: str
    type: str
    topic: str
    user_answer: Optional[str] = None
    correct_answer: str
    is_correct: bool
    explanation: str

class AssessmentResultResponse(BaseModel):
    level_id: str
    skill: str
    level: int
    score: int
    total_questions: int
    percentage: int
    passed: bool
    status: str  # "PASSED" | "FAILED"
    passing_score: int
    attempts_count: int
    topic_performance: Dict[str, Any]
    strengths: List[str]
    weak_topics: List[str]
    recommended_revisions: List[Dict[str, str]]
    suggested_practice: List[str]
    reviews: List[QuestionReviewSchema]
    unlocked_next_level: bool = False
    next_level_id: Optional[str] = None
    message: str

# Legacy verification schemas
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

# ============================================================================
# Progress Dashboard Response Schema
# ============================================================================

class ProgressDashboardResponse(BaseModel):
    user_id: str
    career_title: str
    overall_completion_percentage: int
    skills_progress: Optional[List[Dict[str, Any]]] = []
    levels_progress: Optional[Dict[str, int]] = {}
    topics_completed: int = 0
    topics_remaining: int = 0
    total_learning_hours_completed: float = 0.0
    total_learning_hours_estimated: float = 0.0
    assessment_attempts_total: int = 0
    assessment_average_score: int = 0
    passed_levels_count: int = 0
    total_levels_count: int = 3
    recommended_next_step: Optional[Dict[str, Any]] = None
    weak_topics_to_revise: List[Dict[str, Any]] = []
    phases: Optional[List[Dict[str, Any]]] = []
