from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user
from app.database.connection import get_database

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
async def register(user_in: UserRegister):
    db = get_database()
    if db is not None:
        existing = await db.users.find_one({"email": user_in.email})
        if existing:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        hashed_password = get_password_hash(user_in.password)
        user_doc = {
            "full_name": user_in.full_name,
            "email": user_in.email,
            "password": hashed_password,
            "degree": user_in.degree or "B.Tech",
            "department": user_in.department or "Computer Science"
        }
        res = await db.users.insert_one(user_doc)
        user_id = str(res.inserted_id)

        # Initialize default profile in MongoDB
        profile_doc = {
            "user_id": user_id,
            "full_name": user_in.full_name,
            "degree": user_in.degree or "B.Tech",
            "department": user_in.department or "Computer Science",
            "year_of_study": "Final Year",
            "cgpa": "8.0",
            "technical_skills": {"Python": 60, "JavaScript": 60, "SQL": 60, "Git": 60},
            "soft_skills": ["Problem Solving", "Communication"],
            "interests": ["Artificial Intelligence", "Software Development"],
            "aptitude_scores": {"logical_reasoning": 70, "numerical_ability": 70, "analytical_thinking": 70},
            "target_role": "AI Engineer",
            "preferred_domain": "Artificial Intelligence",
            "is_complete": False
        }
        await db.student_profiles.insert_one(profile_doc)
    else:
        user_id = "mock_user_123"

    access_token = create_access_token(data={"sub": user_id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "full_name": user_in.full_name,
            "email": user_in.email,
            "degree": user_in.degree or "B.Tech",
            "department": user_in.department or "Computer Science"
        }
    }

@router.post("/login", response_model=Token)
async def login(user_in: UserLogin):
    db = get_database()
    if db is not None:
        user = await db.users.find_one({"email": user_in.email})
        if not user or not verify_password(user_in.password, user["password"]):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        user_id = str(user["_id"])
        full_name = user.get("full_name", "Student")
        degree = user.get("degree", "B.Tech")
        department = user.get("department", "Computer Science")
    else:
        # Fallback for local demo
        if user_in.password != "password":
            raise HTTPException(status_code=400, detail="Incorrect credentials")
        user_id = "mock_user_123"
        full_name = "Demo Student"
        degree = "B.Tech"
        department = "Computer Science"

    access_token = create_access_token(data={"sub": user_id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "full_name": full_name,
            "email": user_in.email,
            "degree": degree,
            "department": department
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": str(current_user.get("_id", current_user.get("id"))),
        "full_name": current_user.get("full_name", "Student"),
        "email": current_user.get("email", ""),
        "degree": current_user.get("degree", "B.Tech"),
        "department": current_user.get("department", "Computer Science")
    }
