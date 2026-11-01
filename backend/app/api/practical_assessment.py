from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.schemas.practical_assessment import (
    PracticalAssessmentHistoryItem,
    PracticalAssessmentResponse,
    PracticalAssessmentResult,
    PracticalAssessmentStatus,
    PracticalAssessmentSubmission,
)
from app.services.practical_assessment_service import (
    get_attempt_review,
    get_history,
    get_status,
    start_assessment,
    submit_assessment,
)

router = APIRouter(prefix="/practical-assessment", tags=["Practical Skill Assessment"])


def _user_id(current_user: dict) -> str:
    return str(current_user.get("_id", current_user.get("id")))


@router.get("/status", response_model=PracticalAssessmentStatus)
async def assessment_status(current_user: dict = Depends(get_current_user)):
    try:
        return await get_status(_user_id(current_user))
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@router.post("/questions", response_model=PracticalAssessmentResponse)
async def create_assessment(current_user: dict = Depends(get_current_user)):
    try:
        return await start_assessment(_user_id(current_user))
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@router.post("/submit", response_model=PracticalAssessmentResult)
async def submit_practical_assessment(
    submission: PracticalAssessmentSubmission,
    current_user: dict = Depends(get_current_user),
):
    try:
        return await submit_assessment(
            _user_id(current_user), submission.assessment_id, submission.answers
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except TimeoutError as error:
        raise HTTPException(status_code=408, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@router.get("/history", response_model=list[PracticalAssessmentHistoryItem])
async def assessment_history(current_user: dict = Depends(get_current_user)):
    try:
        return await get_history(_user_id(current_user))
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@router.get("/history/{attempt_id}")
async def assessment_attempt_review(
    attempt_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        result = await get_attempt_review(_user_id(current_user), attempt_id)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    if result is None:
        raise HTTPException(status_code=404, detail="Assessment attempt not found.")
    return result
