from fastapi import APIRouter, Depends
from typing import List
from app.schemas.progress import (
    ProgressOverviewResponse,
    SkillProgressItem,
    EmployabilityProgressResponse,
    EmployabilityHistoryPoint
)
from app.core.security import get_current_user
from app.services.progress_service import (
    get_progress_overview,
    get_skill_progress_list,
    get_employability_progress_data,
    get_employability_history_list
)

router = APIRouter(prefix="/progress", tags=["Feature 6 - Employability Progress Tracker"])

@router.get("", response_model=ProgressOverviewResponse)
async def get_progress(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_progress_overview(user_id)

@router.get("/skills", response_model=List[SkillProgressItem])
async def get_skills_progress(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_skill_progress_list(user_id)

@router.get("/employability", response_model=EmployabilityProgressResponse)
async def get_employability_progress(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_employability_progress_data(user_id)

@router.get("/history", response_model=List[EmployabilityHistoryPoint])
async def get_employability_history(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_employability_history_list(user_id)
