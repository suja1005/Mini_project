from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from app.schemas.roadmap import (
    RoadmapResponse,
    RoadmapTaskSchema,
    RoadmapGenerateRequest,
    ToggleSubtopicRequest,
    ToggleLevelTopicRequest,
    SkillOverviewSchema,
    SkillLevelSchema,
    AssessmentGenerateResponse,
    AssessmentSubmissionRequest,
    AssessmentResultResponse,
    ProgressDashboardResponse,
    QuizQuestionResponse,
    QuizSubmissionRequest,
    QuizResultResponse,
    VerificationAttemptSchema
)
from app.core.security import get_current_user
from app.services.roadmap_service import (
    generate_adaptive_roadmap,
    get_user_roadmap,
    get_skills_overview,
    get_skill_level_detail,
    start_skill_level,
    toggle_level_topic,
    generate_level_assessment,
    submit_level_assessment,
    get_level_assessment_history,
    get_progress_dashboard,
    get_task_by_id,
    start_task,
    toggle_subtopic,
    complete_learning,
    generate_task_questions,
    submit_task_verification,
    get_verification_history
)

router = APIRouter(prefix="/roadmap", tags=["Roadmap Module - Level-Based Learning & Assessment"])

# ==============================================================================
# 1. Level-Based Learning System Endpoints (Primary v2 API)
# ==============================================================================

@router.get("/skills", response_model=List[SkillOverviewSchema])
async def get_skills_route(current_user: dict = Depends(get_current_user)):
    """
    Returns all 7 skills with their 3 levels, status, scores, and progress.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_skills_overview(user_id)

@router.get("/skills/{skill_slug}/levels/{level_num}", response_model=SkillLevelSchema)
async def get_level_detail_route(
    skill_slug: str,
    level_num: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Returns specific level curriculum with detailed topics, practical examples, and practice challenges.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await get_skill_level_detail(user_id, skill_slug, level_num)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/skills/{skill_slug}/levels/{level_num}/start", response_model=SkillLevelSchema)
async def start_level_route(
    skill_slug: str,
    level_num: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Starts a level (sets status to IN_PROGRESS). Enforces prerequisite lock rules.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await start_skill_level(user_id, skill_slug, level_num)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/skills/{skill_slug}/levels/{level_num}/topics/{topic_id}/toggle", response_model=SkillLevelSchema)
async def toggle_level_topic_route(
    skill_slug: str,
    level_num: int,
    topic_id: str,
    body: ToggleLevelTopicRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Toggles topic completion and/or practice challenge completion.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await toggle_level_topic(
            user_id=user_id,
            skill_slug=skill_slug,
            level_num=level_num,
            topic_id=topic_id,
            completed=body.completed,
            practice_completed=body.practice_completed
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/skills/{skill_slug}/levels/{level_num}/assessment/generate", response_model=AssessmentGenerateResponse)
async def generate_assessment_route(
    skill_slug: str,
    level_num: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Generates 20 dynamic questions (15 MCQs + 5 practical application questions) for this level assessment.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await generate_level_assessment(user_id, skill_slug, level_num)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/skills/{skill_slug}/levels/{level_num}/assessment/submit", response_model=AssessmentResultResponse)
async def submit_assessment_route(
    skill_slug: str,
    level_num: int,
    body: AssessmentSubmissionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Submits level assessment answers. Evaluates score, pass/fail (70% criteria),
    unlocks next level if passed, and returns comprehensive strengths, weak topics, and explanations.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await submit_level_assessment(user_id, skill_slug, level_num, body.answers)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/skills/{skill_slug}/levels/{level_num}/assessment/history", response_model=List[Dict[str, Any]])
async def get_assessment_history_route(
    skill_slug: str,
    level_num: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieves all past assessment attempt records and score trajectories for this level.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_level_assessment_history(user_id, skill_slug, level_num)

@router.get("/dashboard", response_model=ProgressDashboardResponse)
async def get_dashboard_route(current_user: dict = Depends(get_current_user)):
    """
    Returns progress analytics across all 7 skills, 21 levels, hours studied, weak topics, and recommendations.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_progress_dashboard(user_id)

# ==============================================================================
# 2. Complete Roadmap & Overview Endpoints
# ==============================================================================

@router.post("/generate", response_model=RoadmapResponse)
async def create_roadmap(
    body: RoadmapGenerateRequest = RoadmapGenerateRequest(),
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    career_id = body.career_id or "ai-engineer"
    return await generate_adaptive_roadmap(user_id, career_id)

@router.get("", response_model=RoadmapResponse)
async def get_roadmap(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_user_roadmap(user_id)

@router.get("/progress", response_model=Dict[str, Any])
async def get_roadmap_progress(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    roadmap = await get_user_roadmap(user_id)
    return {
        "user_id": user_id,
        "career_title": roadmap.get("career_title"),
        "total_tasks": roadmap.get("total_tasks"),
        "verified_tasks": roadmap.get("verified_tasks"),
        "completed_tasks": roadmap.get("completed_tasks"),
        "progress_percentage": roadmap.get("progress_percentage"),
        "current_employability": roadmap.get("current_employability"),
        "target_employability": roadmap.get("target_employability"),
        "employability_gap": roadmap.get("employability_gap")
    }

# ==============================================================================
# 3. Legacy Task Compatibility Routes
# ==============================================================================

@router.get("/tasks/{task_id}", response_model=RoadmapTaskSchema)
async def get_task_detail(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    task = await get_task_by_id(user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/tasks/{task_id}/start", response_model=RoadmapResponse)
async def start_task_route(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await start_task(user_id, task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tasks/{task_id}/topics/toggle", response_model=RoadmapResponse)
async def toggle_topic_route(
    task_id: str,
    body: ToggleSubtopicRequest,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await toggle_subtopic(
            user_id=user_id,
            task_id=task_id,
            topic_id=body.topic_id,
            subtopic_id=body.subtopic_id,
            completed=body.completed
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tasks/{task_id}/complete-learning", response_model=RoadmapResponse)
async def complete_learning_route(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await complete_learning(user_id, task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tasks/{task_id}/generate-questions", response_model=List[QuizQuestionResponse])
async def generate_questions_route(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await generate_task_questions(user_id, task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tasks/{task_id}/submit-verification", response_model=QuizResultResponse)
async def submit_verification_route(
    task_id: str,
    body: QuizSubmissionRequest,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await submit_task_verification(user_id, task_id, body.answers)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tasks/{task_id}/verification-history", response_model=List[VerificationAttemptSchema])
async def get_verification_history_route(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_verification_history(user_id, task_id)
