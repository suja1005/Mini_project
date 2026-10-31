import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.assessment import (
    QuestionSchema,
    AssessmentSubmit,
    AssessmentResultResponse
)
from app.core.security import get_current_user
from app.database.connection import get_database
from app.services.question_generation_service import question_gen_service

router = APIRouter(prefix="/assessment", tags=["Assessment Engine - Dynamic & Personalized"])

@router.get("/questions", response_model=List[QuestionSchema])
async def get_questions(current_user: dict = Depends(get_current_user)):
    """
    Returns personalized, randomized assessment questions tailored to the authenticated
    student's profile (interests, career target, skills, learning phase).
    Avoids questions previously attempted by this student whenever possible.
    Never exposes correct answers.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    db = get_database()

    # 1. Fetch student profile from database
    profile = {}
    if db is not None:
        profile_doc = await db.student_profiles.find_one({"user_id": user_id})
        if profile_doc:
            profile = profile_doc

    # Default fallback profile if not yet onboarded
    if not profile:
        profile = {
            "user_id": user_id,
            "interests": ["Artificial Intelligence", "Software Development"],
            "target_role": "AI Engineer",
            "technical_skills": {"Python": 60, "SQL": 60},
            "academic_background": "Computer Science"
        }

    # 2. Collect previously attempted question IDs for this student
    exclude_ids = []
    if db is not None:
        cursor = db.assessment_attempts.find({"user_id": user_id})
        past_attempts = await cursor.to_list(length=100)
        for att in past_attempts:
            exclude_ids.extend(att.get("question_ids", []))

    # 3. Generate personalized questions
    client_qs, full_qs = question_gen_service.generate_personalized_assessment(
        user_id=user_id,
        profile=profile,
        exclude_ids=exclude_ids,
        total_count=15,
        phase="Beginner"
    )

    # 4. Save active assessment securely in MongoDB
    if db is not None:
        await db.active_quizzes.update_one(
            {"user_id": user_id, "type": "initial_assessment"},
            {"$set": {
                "user_id": user_id,
                "type": "initial_assessment",
                "full_questions": full_qs,
                "created_at": datetime.now(timezone.utc).isoformat()
            }},
            upsert=True
        )

    # Format for response
    results = []
    for q in client_qs:
        results.append(QuestionSchema(
            id=q.get("question_id"),
            question_id=q.get("question_id"),
            question_number=q.get("question_number"),
            category=q.get("skill", "General"),
            skill=q.get("skill", "General"),
            topic=q.get("topic", "General"),
            difficulty=q.get("difficulty", "Beginner"),
            type=q.get("type", "mcq"),
            question=q.get("question"),
            options=q.get("options", [])
        ))

    return results

@router.post("/submit", response_model=AssessmentResultResponse)
async def submit_assessment(
    submission: AssessmentSubmit,
    current_user: dict = Depends(get_current_user)
):
    """
    Evaluates assessment answers strictly on the backend.
    Calculates score: (Correct / Total) * 100.
    Stores attempt and results in MongoDB associated with the authenticated student.
    Updates skill-level estimates in student profile.
    Returns score, correct answers, explanations, and areas for improvement.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    db = get_database()
    now_str = datetime.now(timezone.utc).isoformat()

    # 1. Retrieve the student's active assessment
    active_quiz = None
    if db is not None:
        active_quiz = await db.active_quizzes.find_one({"user_id": user_id, "type": "initial_assessment"})

    full_questions = []
    if active_quiz and "full_questions" in active_quiz:
        full_questions = active_quiz["full_questions"]

    # Fallback if active quiz session expired
    if not full_questions:
        profile = {}
        if db is not None:
            profile = await db.student_profiles.find_one({"user_id": user_id}) or {}
        _, full_questions = question_gen_service.generate_personalized_assessment(
            user_id=user_id,
            profile=profile,
            total_count=15
        )

    # Normalize answers: support both option text and index mappings
    normalized_answers = {}
    for q in full_questions:
        q_id = str(q.get("id", q.get("question_id", "")))
        ans_val = submission.answers.get(q_id)
        if ans_val is None:
            # check by question_number as fallback
            q_num = str(q.get("question_number", ""))
            ans_val = submission.answers.get(q_num)

        if isinstance(ans_val, int) and "options" in q and 0 <= ans_val < len(q["options"]):
            normalized_answers[q_id] = q["options"][ans_val]
        elif ans_val is not None:
            normalized_answers[q_id] = str(ans_val)
        else:
            normalized_answers[q_id] = ""

    # 2. Evaluate answers on backend
    eval_result = question_gen_service.evaluate_assessment(
        full_questions=full_questions,
        student_answers=normalized_answers,
        passing_score=80
    )

    overall_score = eval_result["percentage"]
    correct_count = eval_result["score"]
    total_q = eval_result["total_questions"]

    # Calculate categorical scores for profile update
    topic_perf = eval_result.get("topic_performance", {})
    tech_pct = overall_score
    logic_pct = 75
    num_pct = 75

    for top, stat in topic_perf.items():
        top_lower = top.lower()
        if "logic" in top_lower or "problem" in top_lower:
            logic_pct = stat.get("percentage", 75)
        elif "math" in top_lower or "stat" in top_lower or "numeric" in top_lower:
            num_pct = stat.get("percentage", 75)
        elif "python" in top_lower or "web" in top_lower or "ml" in top_lower:
            tech_pct = stat.get("percentage", tech_pct)

    attempt_id = f"att_{uuid.uuid4().hex[:8]}"
    attempt_doc = {
        "id": attempt_id,
        "attempt_id": attempt_id,
        "user_id": user_id,
        "student_id": user_id,
        "overall_score": overall_score,
        "percentage": overall_score,
        "score": correct_count,
        "total_questions": total_q,
        "correct_count": correct_count,
        "passed": eval_result["passed"],
        "question_ids": [q["id"] for q in full_questions],
        "answers": submission.answers,
        "topic_performance": topic_perf,
        "strengths": eval_result.get("strengths", []),
        "weak_topics": eval_result.get("weak_topics", []),
        "recommended_revisions": eval_result.get("recommended_revisions", []),
        "reviews": eval_result.get("reviews", []),
        "created_at": now_str
    }

    result_doc = {
        "user_id": user_id,
        "overall_score": overall_score,
        "score": correct_count,
        "percentage": overall_score,
        "logical_score": logic_pct,
        "numerical_score": num_pct,
        "technical_score": tech_pct,
        "total_questions": total_q,
        "correct_count": correct_count,
        "passed": eval_result["passed"],
        "is_completed": True,
        "topic_performance": topic_perf,
        "strengths": eval_result.get("strengths", []),
        "weak_topics": eval_result.get("weak_topics", []),
        "recommended_revisions": eval_result.get("recommended_revisions", []),
        "reviews": eval_result.get("reviews", []),
        "last_attempt_id": attempt_id,
        "updated_at": now_str
    }

    if db is not None:
        # Save attempt
        await db.assessment_attempts.insert_one(attempt_doc)

        # Update primary assessment result
        await db.assessment_results.update_one(
            {"user_id": user_id},
            {"$set": result_doc},
            upsert=True
        )

        # Update student profile aptitude and skill scores based on real assessment
        await db.student_profiles.update_one(
            {"user_id": user_id},
            {"$set": {
                "aptitude_scores": {
                    "logical_reasoning": logic_pct,
                    "numerical_ability": num_pct,
                    "analytical_thinking": tech_pct
                },
                "assessment_completed": True,
                "assessment_score": overall_score,
                "assessment_updated_at": now_str
            }}
        )

    return result_doc

@router.get("/results", response_model=AssessmentResultResponse)
async def get_results(current_user: dict = Depends(get_current_user)):
    """
    Returns latest verified assessment results for the authenticated student.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    db = get_database()

    if db is not None:
        res = await db.assessment_results.find_one({"user_id": user_id})
        if res:
            res["user_id"] = user_id
            return res

    return {
        "user_id": user_id,
        "overall_score": 0,
        "score": 0,
        "percentage": 0,
        "logical_score": 70,
        "numerical_score": 70,
        "technical_score": 70,
        "total_questions": 0,
        "correct_count": 0,
        "passed": False,
        "is_completed": False,
        "topic_performance": {},
        "strengths": [],
        "weak_topics": [],
        "reviews": []
    }

@router.get("/history")
async def get_assessment_history(current_user: dict = Depends(get_current_user)):
    """
    Returns full history of assessment attempts for the authenticated student.
    """
    user_id = str(current_user.get("_id", current_user.get("id")))
    db = get_database()
    if db is not None:
        cursor = db.assessment_attempts.find({"user_id": user_id}).sort("created_at", -1)
        attempts = await cursor.to_list(length=50)
        for a in attempts:
            a["_id"] = str(a["_id"])
        return attempts
    return []
