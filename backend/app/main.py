import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add parent directory to python path for smooth relative imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.skills import router as skills_router
from app.api.assessment import router as assessment_router
from app.api.recommendations import router as recommendation_router
from app.api.career_analysis import router as career_analysis_router
from app.api.evidence import router as evidence_router
from app.api.roadmap import router as roadmap_router
from app.api.progress import router as progress_router
from app.database.connection import connect_to_mongo, close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Backend API for AI-Powered Career Guidance and Employability Enhancement Platform",
    version="2.0.0",
    lifespan=lifespan
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers directly under API_V1_STR (/api/v1)
app.include_router(health_router, prefix=settings.API_V1_STR, tags=["Health & System"])
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(profile_router, prefix=settings.API_V1_STR)
app.include_router(skills_router, prefix=settings.API_V1_STR)
app.include_router(assessment_router, prefix=settings.API_V1_STR)
app.include_router(recommendation_router, prefix=settings.API_V1_STR)
app.include_router(career_analysis_router, prefix=settings.API_V1_STR)
app.include_router(evidence_router, prefix=settings.API_V1_STR)
app.include_router(roadmap_router, prefix=settings.API_V1_STR)
app.include_router(progress_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "AI-Powered Career Guidance Platform API",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
