from fastapi import APIRouter, Depends, HTTPException
from app.schemas.profile import StudentProfileSchema, StudentProfileResponse
from app.core.security import get_current_user
from app.database.connection import get_database

router = APIRouter(prefix="/profile", tags=["Student Profile"])

@router.get("", response_model=StudentProfileResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    db = get_database()
    
    if db is not None:
        profile = await db.student_profiles.find_one({"user_id": user_id})
        if profile:
            profile["user_id"] = user_id
            return profile

    # Default baseline profile
    return {
        "user_id": user_id,
        "full_name": current_user.get("full_name", "Demo Student"),
        "degree": current_user.get("degree", "B.Tech"),
        "department": current_user.get("department", "Computer Science"),
        "year_of_study": "Final Year",
        "cgpa": "8.4 CGPA",
        "technical_skills": {
            "Python": 85,
            "Machine Learning": 60,
            "SQL": 60,
            "Git": 70,
            "JavaScript": 60,
            "Data Analysis": 60
        },
        "soft_skills": ["Problem Solving", "Communication", "Teamwork"],
        "interests": ["Artificial Intelligence", "Data Science", "Software Development"],
        "aptitude_scores": {
            "logical_reasoning": 75,
            "numerical_ability": 70,
            "analytical_thinking": 80
        },
        "target_role": "AI Engineer",
        "preferred_domain": "Artificial Intelligence",
        "is_complete": True
    }

@router.put("", response_model=StudentProfileResponse)
async def update_profile(
    profile_in: StudentProfileSchema,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.get("_id", current_user.get("id")))
    db = get_database()

    profile_dict = profile_in.dict()
    profile_dict["user_id"] = user_id
    profile_dict["is_complete"] = True

    if db is not None:
        await db.student_profiles.update_one(
            {"user_id": user_id},
            {"$set": profile_dict},
            upsert=True
        )

    return profile_dict
