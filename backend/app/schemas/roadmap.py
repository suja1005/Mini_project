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
    passing_score: int = 70
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
    passing_score: int = 70
    verification_status: str = "Not Started"
    quiz_score: Optional[int] = None
    attempts_count: int = 0
    learning_progress_percentage: int = 0
    resources: List[RoadmapResourceSchema] = []
    completed_at: Optional[str] = None

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
    skills: List[SkillOverviewSchema] = []
    last_updated: str

# ============================================================================
# Level Assessment Schemas (20 Questions: 15 MCQ + 5 Practical)
# ============================================================================

class AssessmentQuestionClientSchema(BaseModel):
    question_id: str
    question_number: int
    type: str  # "mcq" | "practical"
    question: str
    topic: str
    difficulty: str
    options: List[str] = []
    starter_code: Optional[str] = None
    practical_type: Optional[str] = None  # "code_output", "code_snippet", "sql_query", "numerical", "short_answer"

class AssessmentGenerateResponse(BaseModel):
    level_id: str
    skill: str
    level: int
    total_questions: int = 20
    time_limit_minutes: int = 30
    questions: List[AssessmentQuestionClientSchema]

class AssessmentSubmissionRequest(BaseModel):
    answers: Dict[str, str]  # question_id -> answer

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
    topic_performance: Dict[str, Dict[str, int]]  # topic -> {total, correct, percentage}
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
    skills_progress: List[Dict[str, Any]]
    levels_progress: Dict[str, int]
    topics_completed: int
    topics_remaining: int
    total_learning_hours_completed: float
    total_learning_hours_estimated: float
    assessment_attempts_total: int
    assessment_average_score: int
    passed_levels_count: int
    total_levels_count: int = 21
    recommended_next_step: Optional[Dict[str, Any]] = None
    weak_topics_to_revise: List[Dict[str, Any]] = []
