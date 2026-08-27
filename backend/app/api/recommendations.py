from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from app.schemas.recommendation import RecommendationResponse
from app.core.security import get_current_user
from app.database.connection import get_database
from app.ml.recommendation_engine import generate_user_recommendations

router = APIRouter(prefix="/recommendations", tags=["Multi-Career Recommendations"])

async def get_user_profile_data(user_id: str, current_user: dict) -> dict:
    db = get_database()
    if db is not None:
        profile = await db.student_profiles.find_one({"user_id": user_id})
        if profile:
            return profile

    return {
        "user_id": user_id,
        "full_name": current_user.get("full_name", "Student"),
        "degree": current_user.get("degree", "B.Tech"),
        "technical_skills": {"Python": 85, "Machine Learning": 60, "SQL": 60, "Git": 70},
        "interests": ["Artificial Intelligence", "Data Science"],
        "aptitude_scores": {"logical_reasoning": 80, "numerical_ability": 75, "analytical_thinking": 80},
        "target_role": "AI Engineer"
    }

@router.post("/generate", response_model=RecommendationResponse)
async def generate_recommendations(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    profile = await get_user_profile_data(user_id, current_user)

    top_recs = generate_user_recommendations(profile)
    now_str = datetime.now(timezone.utc).isoformat()

    res_doc = {
        "user_id": user_id,
        "top_recommendations": top_recs,
        "generated_at": now_str
    }

    db = get_database()
    if db is not None:
        await db.recommendations.update_one(
            {"user_id": user_id},
            {"$set": res_doc},
            upsert=True
        )

    return res_doc

@router.get("", response_model=RecommendationResponse)
async def get_recommendations(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    db = get_database()

    if db is not None:
        existing = await db.recommendations.find_one({"user_id": user_id})
        if existing:
            existing["user_id"] = user_id
            return existing

    # Auto-generate if not found
    profile = await get_user_profile_data(user_id, current_user)
    top_recs = generate_user_recommendations(profile)
    now_str = datetime.now(timezone.utc).isoformat()

    return {
        "user_id": user_id,
        "top_recommendations": top_recs,
        "generated_at": now_str
    }
