from fastapi import APIRouter, Depends, HTTPException
from app.schemas.career_analysis import CareerAnalysisResponse
from app.core.security import get_current_user
from app.database.connection import get_database
from app.ml.recommendation_engine import generate_career_analysis, load_careers_data

router = APIRouter(tags=["Career & Risk Analysis"])

@router.get("/careers")
async def get_careers():
    return load_careers_data()

@router.get("/careers/{career_id}")
async def get_career_by_id(career_id: str):
    careers = load_careers_data()
    career = next((c for c in careers if c["id"] == career_id), None)
    if not career:
        raise HTTPException(status_code=404, detail="Career requirement profile not found")
    return career

@router.post("/career-selection/{career_id}")
async def select_career(
    career_id: str,
    current_user: dict = Depends(get_current_user)
):
    careers = load_careers_data()
    career = next((item for item in careers if item.get("id") == career_id), None)
    if not career:
        raise HTTPException(status_code=404, detail="Career requirement profile not found")
    user_id = str(current_user.get("_id", current_user.get("id")))
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Career selection requires an active MongoDB connection.")
    profile = await db.student_profiles.find_one({"user_id": user_id})
    if profile is None:
        raise HTTPException(status_code=409, detail="Complete your student profile before selecting a career.")
    await db.student_profiles.update_one(
        {"user_id": user_id},
        {"$set": {
            "target_role": career["title"],
            "selected_career_id": career_id,
        }}
    )
    return {"career_id": career_id, "target_role": career["title"]}

@router.get("/career-analysis/{career_id}", response_model=CareerAnalysisResponse)
async def get_career_analysis(
    career_id: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    db = get_database()

    profile = None
    if db is not None:
        profile = await db.student_profiles.find_one({"user_id": user_id})

    if not profile:
        profile = {
            "user_id": user_id,
            "full_name": current_user.get("full_name", "Student"),
            "degree": current_user.get("degree", "B.Tech"),
            "technical_skills": {"Python": 70, "Machine Learning": 40, "SQL": 60, "Mathematics": 75, "Communication": 65},
            "interests": ["Artificial Intelligence", "Data Science"],
            "aptitude_scores": {"logical_reasoning": 75, "numerical_ability": 70, "analytical_thinking": 80},
            "target_role": "AI Engineer"
        }

    analysis = generate_career_analysis(profile, career_id)
    return analysis
