from fastapi import APIRouter
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.skills import router as skills_router
from app.api.assessment import router as assessment_router
from app.api.recommendations import router as recommendation_router
from app.api.career_analysis import router as career_analysis_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health & System"])
api_router.include_router(auth_router)
api_router.include_router(profile_router)
api_router.include_router(skills_router)
api_router.include_router(assessment_router)
api_router.include_router(recommendation_router)
api_router.include_router(career_analysis_router)
