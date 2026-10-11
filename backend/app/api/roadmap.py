from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from app.schemas.roadmap import (
    RoadmapResponse,
    RoadmapTaskSchema,
    RoadmapGenerateRequest,
    ToggleSubtopicRequest,
    QuizQuestionResponse,
    QuizSubmissionRequest,
    QuizResultResponse,
    VerificationAttemptSchema
)
from app.core.security import get_current_user
from app.services.roadmap_service import (
    generate_adaptive_roadmap,
    get_user_roadmap,
    get_task_by_id,
    start_task,
    toggle_subtopic,
    complete_learning,
    generate_task_questions,
    submit_task_verification,
    get_verification_history
)

router = APIRouter(prefix="/roadmap", tags=["Roadmap Module - Learning & Verification"])

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
