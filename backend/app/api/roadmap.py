from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from app.database.connection import get_database
from app.schemas.roadmap import (
    RoadmapResponse,
    RoadmapTaskSchema,
    RoadmapGenerateRequest,
    ToggleSubtopicRequest,
    ToggleLevelTopicRequest,
    CompleteTopicRequest,
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
from app.services.career_roadmap_service import (
    get_or_initialize_user_roadmap,
    get_topic_learning_material,
    complete_topic,
    generate_phase_assessment,
    submit_phase_assessment,
    get_phase_assessment_history,
    PASSING_SCORE_THRESHOLD
)
from app.services.roadmap_service import (
    generate_adaptive_roadmap as legacy_generate_adaptive_roadmap,
    get_user_roadmap as legacy_get_user_roadmap,
    get_skills_overview,
    get_skill_level_detail,
    start_skill_level,
    toggle_level_topic,
    generate_level_assessment,
    submit_level_assessment,
    get_level_assessment_history,
    get_progress_dashboard as legacy_get_progress_dashboard,
    get_task_by_id,
    start_task,
    toggle_subtopic,
    complete_learning,
    generate_task_questions,
    submit_task_verification,
    get_verification_history
)

router = APIRouter(prefix="/roadmap", tags=["Adaptive Employability Roadmap (3-Phase)"])

# ==============================================================================
# 1. 3-Phase Career Roadmap Endpoints (Primary Adaptive Engine)
# ==============================================================================

@router.get("", response_model=RoadmapResponse)
async def get_roadmap(current_user: dict = Depends(get_current_user)):
    """
    Returns the authenticated student's personalized 3-phase career roadmap:
    Beginner (Phase 1), Intermediate (Phase 2), and Advanced (Phase 3).
    Includes modules, completion status, locking status, and progress metrics.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_or_initialize_user_roadmap(user_id)

@router.post("/generate", response_model=RoadmapResponse)
async def create_roadmap(
    body: RoadmapGenerateRequest = RoadmapGenerateRequest(),
    current_user: dict = Depends(get_current_user)
):
    """
    Initializes or regenerates a 3-phase roadmap for the specified target career.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    career_id = body.career_id or "ai-engineer"
    return await get_or_initialize_user_roadmap(user_id, career_id)

@router.get("/progress", response_model=Dict[str, Any])
async def get_roadmap_progress(current_user: dict = Depends(get_current_user)):
    """
    Returns high-level roadmap progress metrics calculated directly from database records.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    roadmap = await get_or_initialize_user_roadmap(user_id)
    return {
        "user_id": user_id,
        "career_title": roadmap.get("career_title"),
        "overall_progress": roadmap.get("overall_progress", 0),
        "progress_percentage": roadmap.get("overall_progress", 0),
        "completed_topics_count": roadmap.get("completed_topics_count", 0),
        "total_topics_count": roadmap.get("total_topics_count", 0),
        "next_recommended_action": roadmap.get("next_recommended_action")
    }

@router.get("/dashboard", response_model=Dict[str, Any])
async def get_roadmap_dashboard(current_user: dict = Depends(get_current_user)):
    """
    Returns professional roadmap dashboard analytics including overall progress,
    phase breakdowns, completed/pending topics, best scores, and recommended actions.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    roadmap = await get_or_initialize_user_roadmap(user_id)
    return {
        "user_id": user_id,
        "career_id": roadmap.get("career_id"),
        "career_title": roadmap.get("career_title"),
        "overall_progress": roadmap.get("overall_progress", 0),
        "progress_percentage": roadmap.get("overall_progress", 0),
        "phases": roadmap.get("phases", []),
        "completed_topics": roadmap.get("completed_topics", []),
        "pending_topics": roadmap.get("pending_topics", []),
        "current_learning_topic": roadmap.get("current_learning_topic"),
        "next_recommended_action": roadmap.get("next_recommended_action"),
        "passing_score_requirement": PASSING_SCORE_THRESHOLD
    }

@router.get("/dashboard/summary", response_model=Dict[str, Any])
async def get_dashboard_summary(current_user: dict = Depends(get_current_user)):
    """
    Returns a comprehensive dashboard summary for the authenticated student:
    student name, roadmap progress, phase-wise statuses and scores, activity counts.
    All data is sourced from real MongoDB records of the authenticated user.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    student_name = current_user.get("full_name", "Student")
    db = get_database()

    roadmap = await get_or_initialize_user_roadmap(user_id)
    phases = roadmap.get("phases", [])

    # Current active phase (first AVAILABLE/IN_PROGRESS phase)
    current_phase_name = "Beginner"
    for p in phases:
        if p.get("status") in ("AVAILABLE", "IN_PROGRESS"):
            current_phase_name = p.get("name", "Beginner")
            break

    completed_phases = [p for p in phases if p.get("status") == "COMPLETED"]

    # In-progress topics: incomplete topics in the current active phase only
    in_progress_count = 0
    for p in phases:
        if p.get("status") not in ("LOCKED", "COMPLETED"):
            in_progress_count = p.get("total_topics_count", 0) - p.get("completed_topics_count", 0)
            break

    total_attempts = sum(p.get("attempts_count", 0) for p in phases)

    latest_score = None
    if db is not None:
        last_attempt = await db.phase_assessments.find_one(
            {"user_id": user_id},
            sort=[("created_at", -1)]
        )
        if last_attempt:
            latest_score = last_attempt.get("percentage")

    phase_summaries = []
    for p in phases:
        phase_summaries.append({
            "phase_id": p.get("phase_id"),
            "name": p.get("name"),
            "status": p.get("status"),
            "progress_percentage": p.get("progress_percentage", 0),
            "completed_topics_count": p.get("completed_topics_count", 0),
            "total_topics_count": p.get("total_topics_count", 0),
            "best_score": p.get("best_score"),
            "attempts_count": p.get("attempts_count", 0),
            "assessment_eligible": p.get("assessment_eligible", False),
            "assessment_passed": p.get("assessment_passed", False),
        })

    return {
        "student_name": student_name,
        "career_id": roadmap.get("career_id"),
        "career_title": roadmap.get("career_title"),
        "overall_progress": roadmap.get("overall_progress", 0),
        "completed_topics_count": roadmap.get("completed_topics_count", 0),
        "total_topics_count": roadmap.get("total_topics_count", 0),
        "in_progress_topics_count": in_progress_count,
        "pending_topics_count": max(0, roadmap.get("total_topics_count", 0) - roadmap.get("completed_topics_count", 0) - in_progress_count),
        "completed_phases_count": len(completed_phases),
        "current_phase_name": current_phase_name,
        "total_assessment_attempts": total_attempts,
        "latest_assessment_score": latest_score,
        "next_recommended_action": roadmap.get("next_recommended_action"),
        "phases": phase_summaries,
        "passing_score_requirement": PASSING_SCORE_THRESHOLD
    }

@router.get("/dashboard/recent-activity", response_model=List[Dict[str, Any]])
async def get_recent_activity(current_user: dict = Depends(get_current_user)):
    """
    Returns real recent learning activities for the authenticated student.
    Combines topic completions and phase assessment results, sorted by most recent (up to 15).
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    db = get_database()
    activities = []

    if db is not None:
        cursor = db.topic_completions.find(
            {"user_id": user_id, "completed": True}
        ).sort("completed_at", -1).limit(10)
        completions = await cursor.to_list(length=10)
        for c in completions:
            activities.append({
                "type": "topic_completion",
                "icon": "check",
                "title": f"Completed: {c.get('module_title', 'Topic')}",
                "description": f"Phase: {c.get('phase_id', '').replace('-', ' ').title()}",
                "timestamp": c.get("completed_at"),
                "color": "green"
            })

        cursor = db.phase_assessments.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(10)
        assessments = await cursor.to_list(length=10)
        for a in assessments:
            passed = a.get("passed", False)
            pct = a.get("percentage", 0)
            phase_name = a.get("phase_name", "Phase")
            activities.append({
                "type": "assessment",
                "icon": "award" if passed else "x-circle",
                "title": f"{'Passed' if passed else 'Attempted'}: {phase_name} Assessment",
                "description": f"Score: {pct}% ({'Passed \u2713' if passed else f'Need {PASSING_SCORE_THRESHOLD}% to pass'})",
                "timestamp": a.get("created_at"),
                "color": "green" if passed else "orange"
            })

    activities.sort(key=lambda x: x.get("timestamp") or "", reverse=True)
    return activities[:15]

# ==============================================================================
# 2. Topic Learning Page & Completion Endpoints
# ==============================================================================

@router.get("/topics/{phase_id}/{topic_id}")
async def get_topic_materials(
    phase_id: str,
    topic_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Returns rich learning materials for a specific topic.
    Strictly verifies on the backend that the phase is unlocked.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await get_topic_learning_material(user_id, phase_id, topic_id)
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))

@router.post("/topics/{phase_id}/{topic_id}/complete")
async def complete_topic_route(
    phase_id: str,
    topic_id: str,
    body: CompleteTopicRequest = CompleteTopicRequest(),
    current_user: dict = Depends(get_current_user)
):
    """
    Marks a topic as completed when the student completes the required learning activities.
    Enforces that the phase is not locked and persists completion in MongoDB.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await complete_topic(user_id, phase_id, topic_id, body.practice_answer)
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

# ==============================================================================
# 3. Phase Assessment Endpoints (80% Passing Requirement & Phase Unlocking)
# ==============================================================================

@router.post("/phases/{phase_id}/assessment/generate")
async def generate_phase_assessment_route(
    phase_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Generates randomized questions for a phase assessment.
    Verifies that:
    1. Phase is NOT locked.
    2. All topics in this phase have been completed.
    3. Excludes previously attempted questions by this student when possible.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await generate_phase_assessment(user_id, phase_id)
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@router.post("/phases/{phase_id}/assessment/submit")
async def submit_phase_assessment_route(
    phase_id: str,
    body: AssessmentSubmissionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Submits and validates phase assessment answers strictly on the backend.
    Pass condition: Score Percentage >= 80%.
    Unlocks next phase only upon achieving >= 80%.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await submit_phase_assessment(user_id, phase_id, body.answers)
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@router.get("/phases/{phase_id}/assessment/history")
async def get_phase_assessment_history_route(
    phase_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieves past phase assessment attempts for the authenticated student.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_phase_assessment_history(user_id, phase_id)

# ==============================================================================
# 4. Level-Based Learning Endpoints (Preserved for full compatibility)
# ==============================================================================

@router.get("/skills", response_model=List[SkillOverviewSchema])
async def get_skills_route(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_skills_overview(user_id)

@router.get("/skills/{skill_slug}/levels/{level_num}", response_model=SkillLevelSchema)
async def get_level_detail_route(
    skill_slug: str,
    level_num: int,
    current_user: dict = Depends(get_current_user)
):
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
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_level_assessment_history(user_id, skill_slug, level_num)

# ==============================================================================
# 5. Legacy Task Compatibility Routes
# ==============================================================================

@router.get("/tasks/{task_id}", response_model=RoadmapTaskSchema)
async def get_task_detail(task_id: str, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await get_task_by_id(user_id, task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/tasks/{task_id}/start", response_model=RoadmapResponse)
async def start_task_action(task_id: str, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        await start_task(user_id, task_id)
        return await get_or_initialize_user_roadmap(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tasks/{task_id}/topics/toggle", response_model=RoadmapResponse)
async def toggle_subtopic_action(
    task_id: str,
    body: ToggleSubtopicRequest,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        await toggle_subtopic(user_id, task_id, body.topic_id, body.subtopic_id, body.completed)
        return await get_or_initialize_user_roadmap(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tasks/{task_id}/complete-learning", response_model=RoadmapResponse)
async def complete_learning_action(task_id: str, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        await complete_learning(user_id, task_id)
        return await get_or_initialize_user_roadmap(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tasks/{task_id}/generate-questions", response_model=List[QuizQuestionResponse])
async def generate_quiz_action(task_id: str, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    try:
        return await generate_task_questions(user_id, task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tasks/{task_id}/submit-verification", response_model=QuizResultResponse)
async def submit_quiz_action(
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
async def get_task_history_action(task_id: str, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_verification_history(user_id, task_id)
