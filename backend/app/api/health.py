from fastapi import APIRouter
from app.schemas.health import HealthResponse
from app.database.connection import db_instance

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    db_connected = False
    if db_instance.client is not None:
        try:
            await db_instance.client.admin.command('ping')
            db_connected = True
        except Exception:
            db_connected = False

    return HealthResponse(
        status="healthy",
        version="2.0.0-phase2",
        service="AI-Powered Career Guidance & Employability Enhancement Platform API",
        database_connected=db_connected,
        phase="Phase 2 - Evidence-Based Employability Enhancement",
        active_modules={
            "Module A - Authentication": True,
            "Module B - AI Student Profile": True,
            "Module C - Assessment Engine": True,
            "Module D - Multi-Career Recommendation": True,
            "Module E - Basic Decision & Risk Analysis": True,
            "Module F - Evidence Engine": True,
            "Module G - Adaptive Roadmap": True,
            "Module H - Progress Tracker": True
        }
    )
