from fastapi import APIRouter, Depends, HTTPException
from app.schemas.evidence import (
    ProjectEvidenceCreate,
    ProjectEvidenceResponse,
    EvidenceOverviewResponse,
    VerifiedSkillsResponse,
    SkillEvidenceItem
)
from app.core.security import get_current_user
from app.services.evidence_service import (
    get_or_create_user_evidence,
    add_project_evidence,
    get_verified_skills_dict
)

router = APIRouter(tags=["Feature 4 - Evidence Engine"])

@router.get("/evidence", response_model=EvidenceOverviewResponse)
async def get_evidence(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_or_create_user_evidence(user_id)

@router.post("/evidence/project", response_model=ProjectEvidenceResponse)
async def create_project_evidence(
    project_in: ProjectEvidenceCreate,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await add_project_evidence(user_id, project_in.dict())

@router.get("/evidence/{skill_name}", response_model=SkillEvidenceItem)
async def get_skill_evidence(
    skill_name: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    overview = await get_or_create_user_evidence(user_id)
    for s in overview["skills"]:
        if s["skill"].lower() == skill_name.lower():
            return s
    raise HTTPException(status_code=404, detail=f"No evidence record found for skill '{skill_name}'")

@router.get("/verified-skills", response_model=VerifiedSkillsResponse)
async def get_verified_skills(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    overview = await get_or_create_user_evidence(user_id)
    v_skills = {}
    conf_map = {}
    for s in overview["skills"]:
        v_skills[s["skill"]] = s["verified_score"]
        conf_map[s["skill"]] = s["confidence"]
    return {
        "user_id": user_id,
        "verified_skills": v_skills,
        "confidence_levels": conf_map
    }

@router.post("/evidence/recalculate", response_model=EvidenceOverviewResponse)
async def recalculate_evidence(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return await get_or_create_user_evidence(user_id)
