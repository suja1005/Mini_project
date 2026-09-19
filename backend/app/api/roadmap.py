from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.roadmap import (
    RoadmapResponse,
    RoadmapTaskSchema,
    RoadmapTaskUpdate,
    RoadmapGenerateRequest
)
from app.core.security import get_current_user
from app.services.roadmap_service import (
    generate_adaptive_roadmap,
    get_user_roadmap,
    update_task_status,
    complete_task_and_recalculate
)

router = APIRouter(prefix="/roadmap", tags=["Feature 5 - Adaptive Employability Roadmap"])

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

@router.get("/tasks", response_model=List[RoadmapTaskSchema])
async def get_tasks(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    roadmap = await get_user_roadmap(user_id)
    return roadmap.get("tasks", [])

@router.put("/tasks/{task_id}", response_model=RoadmapResponse)
async def update_task(
    task_id: str,
    update_in: RoadmapTaskUpdate,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await update_task_status(user_id, task_id, update_in.status)

@router.post("/tasks/{task_id}/complete", response_model=RoadmapResponse)
async def complete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await complete_task_and_recalculate(user_id, task_id)
