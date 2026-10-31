"""
Service managing 3-Phase Career Adaptive Roadmap:
- Beginner, Intermediate, and Advanced Phases
- Strict Backend-Enforced Phase Locking
- Real MongoDB Persistence isolated by authenticated user ID
- Topic Completion Tracking with Green Indicators
- Phase Assessments with strict 80% passing threshold
- Comprehensive Progress Dashboard Analytics
"""
import uuid
import random
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple

from app.database.connection import get_database
from app.services.career_roadmap_curriculum import get_career_curriculum
from app.services.question_generation_service import question_gen_service

PASSING_SCORE_THRESHOLD = 80  # Mandatory 80% passing requirement

async def get_or_initialize_user_roadmap(user_id: str, career_id: str = "ai-engineer") -> Dict[str, Any]:
    """
    Retrieves or generates the authenticated student's 3-phase roadmap.
    Beginner phase starts AVAILABLE. Intermediate & Advanced start LOCKED.
    All data is isolated by user_id and persisted in MongoDB.
    """
    db = get_database()
    now_str = datetime.now(timezone.utc).isoformat()

    # Find student profile to obtain career target if not provided
    if db is not None:
        profile = await db.student_profiles.find_one({"user_id": user_id})
        if profile and profile.get("target_role"):
            target_slug = profile.get("target_role").lower().replace(" ", "-")
            if target_slug in ["ai-engineer", "data-scientist", "web-developer"]:
                career_id = target_slug

    curriculum = get_career_curriculum(career_id)

    # Check existing roadmap in DB
    existing_rm = None
    if db is not None:
        existing_rm = await db.career_roadmaps.find_one({"user_id": user_id})

    # Fetch all completed topic IDs for this user
    completed_topics_map = {}
    if db is not None:
        cursor = db.topic_completions.find({"user_id": user_id, "completed": True})
        completions = await cursor.to_list(length=200)
        for c in completions:
            completed_topics_map[c["topic_id"]] = c

    # Fetch phase assessment history / best scores
    phase_assessments_map = {}
    if db is not None:
        cursor = db.phase_assessments.find({"user_id": user_id})
        past_assessments = await cursor.to_list(length=100)
        for pa in past_assessments:
            p_id = pa["phase_id"]
            if p_id not in phase_assessments_map:
                phase_assessments_map[p_id] = []
            phase_assessments_map[p_id].append(pa)

    # Determine phase completion states
    # Phase 1 is completed if it has a passing assessment (>= 80%)
    p1_passed = any(a.get("percentage", 0) >= PASSING_SCORE_THRESHOLD for a in phase_assessments_map.get("phase-1", []))
    p2_passed = any(a.get("percentage", 0) >= PASSING_SCORE_THRESHOLD for a in phase_assessments_map.get("phase-2", []))
    p3_passed = any(a.get("percentage", 0) >= PASSING_SCORE_THRESHOLD for a in phase_assessments_map.get("phase-3", []))

    # Phase 1: Unlocked by default
    p1_status = "COMPLETED" if p1_passed else "AVAILABLE"

    # Phase 2: Strictly LOCKED until Phase 1 is passed
    if p1_passed:
        p2_status = "COMPLETED" if p2_passed else "AVAILABLE"
    else:
        p2_status = "LOCKED"

    # Phase 3: Strictly LOCKED until Phase 2 is passed
    if p1_passed and p2_passed:
        p3_status = "COMPLETED" if p3_passed else "AVAILABLE"
    else:
        p3_status = "LOCKED"

    status_by_phase = {
        "phase-1": p1_status,
        "phase-2": p2_status,
        "phase-3": p3_status
    }

    # Build enriched phases
    phases_out = []
    total_topics_count = 0
    total_completed_count = 0
    completed_topics_list = []
    pending_topics_list = []
    current_learning_topic = None

    for p in curriculum["phases"]:
        p_id = p["phase_id"]
        p_status = status_by_phase.get(p_id, "LOCKED")
        p_attempts = phase_assessments_map.get(p_id, [])
        best_score = max([a.get("percentage", 0) for a in p_attempts], default=None)
        latest_attempt = p_attempts[-1] if p_attempts else None

        modules_out = []
        phase_completed_topics = 0

        for m in p["modules"]:
            total_topics_count += 1
            t_id = m["id"]
            is_done = t_id in completed_topics_map
            comp_record = completed_topics_map.get(t_id)

            if is_done:
                phase_completed_topics += 1
                total_completed_count += 1
                completed_topics_list.append({
                    "id": t_id,
                    "title": m["module_title"],
                    "phase_id": p_id,
                    "completed_at": comp_record.get("completed_at")
                })
            else:
                pending_topics_list.append({
                    "id": t_id,
                    "title": m["module_title"],
                    "phase_id": p_id
                })
                if p_status != "LOCKED" and current_learning_topic is None:
                    current_learning_topic = {
                        "id": t_id,
                        "title": m["module_title"],
                        "phase_id": p_id,
                        "phase_name": p["name"],
                        "estimated_duration": m["estimated_duration"]
                    }

            mod_status = "LOCKED"
            if p_status != "LOCKED":
                mod_status = "COMPLETED" if is_done else "AVAILABLE"

            modules_out.append({
                "id": t_id,
                "module_title": m["module_title"],
                "topic_title": m["topic_title"],
                "estimated_duration": m["estimated_duration"],
                "learning_objectives": m["learning_objectives"],
                "completed": is_done,
                "status": mod_status,
                "completed_at": comp_record.get("completed_at") if comp_record else None
            })

        num_modules = len(p["modules"])
        p_pct = int(round((phase_completed_topics / float(num_modules)) * 100)) if num_modules > 0 else 0
        if p_status == "COMPLETED":
            p_pct = 100

        all_topics_in_phase_done = (phase_completed_topics == num_modules and num_modules > 0)

        phases_out.append({
            "phase_id": p_id,
            "phase_number": p["phase_number"],
            "name": p["name"],
            "difficulty": p["difficulty"],
            "description": p["description"],
            "status": p_status,
            "is_locked": (p_status == "LOCKED"),
            "progress_percentage": p_pct,
            "completed_topics_count": phase_completed_topics,
            "total_topics_count": num_modules,
            "all_topics_completed": all_topics_in_phase_done,
            "assessment_eligible": all_topics_in_phase_done and (p_status != "LOCKED"),
            "assessment_passed": (p_status == "COMPLETED"),
            "best_score": best_score,
            "attempts_count": len(p_attempts),
            "passing_score": PASSING_SCORE_THRESHOLD,
            "unlock_requirement": (
                "Unlocked" if p_id == "phase-1" else
                (f"Complete {curriculum['phases'][p['phase_number']-2]['name']} with score >= {PASSING_SCORE_THRESHOLD}%")
            ),
            "modules": modules_out
        })

    # Overall progress: weighted calculation based on completed topics and passed phases
    overall_pct = int(round((total_completed_count / float(total_topics_count or 1)) * 60))
    passed_phases_count = sum(1 for p in phases_out if p["status"] == "COMPLETED")
    overall_pct += int(round((passed_phases_count / 3.0) * 40))
    overall_pct = min(100, max(0, overall_pct))

    # Determine next recommended action
    next_action = "Begin studying Beginner Phase topics"
    if p3_passed:
        next_action = "Congratulations! You have mastered all 3 phases of the career roadmap."
    elif p2_passed:
        if phases_out[2]["all_topics_completed"]:
            next_action = "Take the Advanced Phase Assessment to graduate!"
        else:
            next_action = f"Study next Advanced topic: {pending_topics_list[0]['title'] if pending_topics_list else 'Final Topics'}"
    elif p1_passed:
        if phases_out[1]["all_topics_completed"]:
            next_action = "Take the Intermediate Phase Assessment (Score >= 80% to unlock Advanced)"
        else:
            next_action = f"Study next Intermediate topic: {pending_topics_list[0]['title'] if pending_topics_list else 'Intermediate Topics'}"
    else:
        if phases_out[0]["all_topics_completed"]:
            next_action = "Take the Beginner Phase Assessment (Score >= 80% to unlock Intermediate)"
        else:
            next_action = f"Study next Beginner topic: {pending_topics_list[0]['title'] if pending_topics_list else 'Python Fundamentals'}"

    roadmap_doc = {
        "user_id": user_id,
        "career_id": career_id,
        "career_title": curriculum["career_title"],
        "description": curriculum["description"],
        "overall_progress": overall_pct,
        "progress_percentage": overall_pct,
        "completed_topics_count": total_completed_count,
        "total_topics_count": total_topics_count,
        "phases": phases_out,
        "completed_topics": completed_topics_list,
        "pending_topics": pending_topics_list,
        "current_learning_topic": current_learning_topic,
        "next_recommended_action": next_action,
        "passing_score_requirement": PASSING_SCORE_THRESHOLD,
        "last_updated": now_str
    }

    if db is not None:
        await db.career_roadmaps.update_one(
            {"user_id": user_id},
            {"$set": roadmap_doc},
            upsert=True
        )

    return roadmap_doc

async def get_topic_learning_material(user_id: str, phase_id: str, topic_id: str) -> Dict[str, Any]:
    """
    Returns rich learning materials for a specific module.
    Backend verifies that the phase is not locked before returning content.
    """
    roadmap = await get_or_initialize_user_roadmap(user_id)
    target_phase = next((p for p in roadmap["phases"] if p["phase_id"] == phase_id), None)
    if not target_phase:
        raise ValueError(f"Phase '{phase_id}' not found.")

    # Strict phase lock enforcement on backend
    if target_phase["status"] == "LOCKED":
        raise PermissionError(
            f"Cannot access {target_phase['name']}. "
            f"Requirement: {target_phase['unlock_requirement']}."
        )

    # Locate module in curriculum
    curriculum = get_career_curriculum(roadmap["career_id"])
    curr_phase = next((p for p in curriculum["phases"] if p["phase_id"] == phase_id), None)
    curr_module = next((m for m in curr_phase["modules"] if m["id"] == topic_id), None) if curr_phase else None

    if not curr_module:
        raise ValueError(f"Module '{topic_id}' not found in {phase_id}.")

    # Check if student has completed this topic
    db = get_database()
    is_completed = False
    completed_at = None
    if db is not None:
        rec = await db.topic_completions.find_one({"user_id": user_id, "topic_id": topic_id, "completed": True})
        if rec:
            is_completed = True
            completed_at = rec.get("completed_at")

    materials = curr_module["learning_materials"]

    return {
        "user_id": user_id,
        "phase_id": phase_id,
        "phase_name": curr_phase["name"],
        "topic_id": topic_id,
        "module_title": curr_module["module_title"],
        "topic_title": curr_module["topic_title"],
        "estimated_duration": curr_module["estimated_duration"],
        "learning_objectives": curr_module["learning_objectives"],
        "completed": is_completed,
        "completed_at": completed_at,
        "lesson": materials.get("lesson", ""),
        "step_by_step_explanation": materials.get("step_by_step_explanation", []),
        "code_examples": materials.get("code_examples", []),
        "practical_exercises": materials.get("practical_exercises", []),
        "documentation": materials.get("documentation", []),
        "curated_videos": materials.get("curated_videos", []),
        "mini_project": materials.get("mini_project", {}),
        "knowledge_check": {
            "question": materials.get("knowledge_check", {}).get("question", ""),
            "options": materials.get("knowledge_check", {}).get("options", []),
            # Do NOT expose correct answer in regular view
        }
    }

async def complete_topic(
    user_id: str,
    phase_id: str,
    topic_id: str,
    practice_answer: Optional[str] = None
) -> Dict[str, Any]:
    """
    Marks a topic as completed when the student finishes required activities.
    Does NOT mark complete merely upon opening the page!
    Enforces that the phase is not locked.
    Persists completion in MongoDB with student_id, roadmap_id, phase_id, topic_id, timestamp.
    """
    roadmap = await get_or_initialize_user_roadmap(user_id)
    target_phase = next((p for p in roadmap["phases"] if p["phase_id"] == phase_id), None)
    if not target_phase:
        raise ValueError(f"Phase '{phase_id}' not found.")

    if target_phase["status"] == "LOCKED":
        raise PermissionError(f"Cannot complete topics in a locked phase ({target_phase['name']}).")

    curriculum = get_career_curriculum(roadmap["career_id"])
    curr_phase = next((p for p in curriculum["phases"] if p["phase_id"] == phase_id), None)
    curr_module = next((m for m in curr_phase["modules"] if m["id"] == topic_id), None) if curr_phase else None

    if not curr_module:
        raise ValueError(f"Module '{topic_id}' not found.")

    # Validate knowledge check practice answer if provided
    correct_ans = curr_module["learning_materials"].get("knowledge_check", {}).get("correct_answer")
    if practice_answer and correct_ans:
        if practice_answer.strip().lower() != correct_ans.strip().lower():
            raise ValueError(f"Practice check answer is incorrect. Review the lesson and try again.")

    db = get_database()
    now_str = datetime.now(timezone.utc).isoformat()

    record = {
        "user_id": user_id,
        "student_id": user_id,
        "roadmap_id": f"rm_{user_id}_{roadmap['career_id']}",
        "phase_id": phase_id,
        "topic_id": topic_id,
        "module_title": curr_module["module_title"],
        "completed": True,
        "completed_at": now_str,
        "assessment_status": "COMPLETED"
    }

    if db is not None:
        await db.topic_completions.update_one(
            {"user_id": user_id, "topic_id": topic_id},
            {"$set": record},
            upsert=True
        )

    # Return refreshed roadmap state
    refreshed_rm = await get_or_initialize_user_roadmap(user_id, roadmap["career_id"])
    return {
        "success": True,
        "message": f"Topic '{curr_module['module_title']}' marked as COMPLETED.",
        "topic_id": topic_id,
        "completed": True,
        "completed_at": now_str,
        "roadmap": refreshed_rm
    }

async def generate_phase_assessment(user_id: str, phase_id: str) -> Dict[str, Any]:
    """
    Generates randomized questions for a phase assessment.
    Backend verifies:
    1. Phase is NOT locked.
    2. ALL topics in this phase have been completed by the student.
    3. Excludes previously attempted questions by this student when alternatives exist.
    4. Passing requirement is 80%.
    """
    roadmap = await get_or_initialize_user_roadmap(user_id)
    target_phase = next((p for p in roadmap["phases"] if p["phase_id"] == phase_id), None)
    if not target_phase:
        raise ValueError(f"Phase '{phase_id}' not found.")

    # 1. Phase locking verification
    if target_phase["status"] == "LOCKED":
        raise PermissionError(
            f"Cannot take assessment for locked phase. {target_phase['unlock_requirement']}."
        )

    # 2. Topic completion verification: all required topics must be complete
    if not target_phase["all_topics_completed"]:
        uncompleted = [m["module_title"] for m in target_phase["modules"] if not m["completed"]]
        raise ValueError(
            f"You must study and complete all topics in {target_phase['name']} before attempting the assessment. "
            f"Incomplete topics: {', '.join(uncompleted)}."
        )

    # 3. Gather past question IDs to avoid repeats
    db = get_database()
    used_ids = []
    if db is not None:
        cursor = db.phase_assessments.find({"user_id": user_id, "phase_id": phase_id})
        past = await cursor.to_list(length=100)
        for att in past:
            used_ids.extend(att.get("question_ids", []))

    # Generate 10 randomized questions matching phase topics and difficulty
    level_num = target_phase["phase_number"]
    phase_difficulty = target_phase["difficulty"]
    
    # Candidate skills for this phase
    profile = {}
    if db is not None:
        profile = await db.student_profiles.find_one({"user_id": user_id}) or {}

    client_qs, full_qs = question_gen_service.generate_personalized_assessment(
        user_id=user_id,
        profile=profile,
        exclude_ids=used_ids,
        total_count=10,
        phase=phase_difficulty
    )

    # Store full questions securely in active_quizzes
    if db is not None:
        await db.active_quizzes.update_one(
            {"user_id": user_id, "phase_id": phase_id},
            {"$set": {
                "user_id": user_id,
                "phase_id": phase_id,
                "career_id": roadmap["career_id"],
                "full_questions": full_qs,
                "passing_score": PASSING_SCORE_THRESHOLD,
                "created_at": datetime.now(timezone.utc).isoformat()
            }},
            upsert=True
        )

    return {
        "phase_id": phase_id,
        "phase_name": target_phase["name"],
        "difficulty": phase_difficulty,
        "total_questions": len(client_qs),
        "passing_score": PASSING_SCORE_THRESHOLD,
        "passing_requirement": f"Score {PASSING_SCORE_THRESHOLD}% or higher to pass",
        "questions": client_qs
    }

async def submit_phase_assessment(
    user_id: str,
    phase_id: str,
    answers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Submits and validates phase assessment answers strictly on the backend.
    Formula: Score Percentage = (Correct Answers / Total Questions) * 100
    Passing requirement: Score Percentage >= 80%
    If passed:
      - Marks phase as COMPLETED
      - Unlocks next phase (Intermediate or Advanced)
    If failed:
      - Keeps current phase incomplete
      - Keeps next phase strictly LOCKED
      - Provides weak topics and revision recommendations
    """
    roadmap = await get_or_initialize_user_roadmap(user_id)
    target_phase = next((p for p in roadmap["phases"] if p["phase_id"] == phase_id), None)
    if not target_phase:
        raise ValueError(f"Phase '{phase_id}' not found.")

    if target_phase["status"] == "LOCKED":
        raise PermissionError(f"Cannot submit assessment for locked phase.")

    db = get_database()
    active_quiz = None
    if db is not None:
        active_quiz = await db.active_quizzes.find_one({"user_id": user_id, "phase_id": phase_id})

    full_questions = active_quiz.get("full_questions", []) if active_quiz else []
    if not full_questions:
        # Fallback question generation if session was lost
        profile = {}
        if db is not None:
            profile = await db.student_profiles.find_one({"user_id": user_id}) or {}
        _, full_questions = question_gen_service.generate_personalized_assessment(
            user_id=user_id,
            profile=profile,
            total_count=10,
            phase=target_phase["difficulty"]
        )

    # Evaluate answers on backend
    eval_result = question_gen_service.evaluate_assessment(
        full_questions=full_questions,
        student_answers=answers,
        passing_score=PASSING_SCORE_THRESHOLD
    )

    percentage = eval_result["percentage"]
    passed = (percentage >= PASSING_SCORE_THRESHOLD)
    now_str = datetime.now(timezone.utc).isoformat()

    # Count prior attempts
    attempts_count = 1
    if db is not None:
        prior_cnt = await db.phase_assessments.count_documents({"user_id": user_id, "phase_id": phase_id})
        attempts_count = prior_cnt + 1

    attempt_doc = {
        "id": f"phase_att_{uuid.uuid4().hex[:8]}",
        "user_id": user_id,
        "student_id": user_id,
        "career_id": roadmap["career_id"],
        "phase_id": phase_id,
        "phase_name": target_phase["name"],
        "attempt_number": attempts_count,
        "score": eval_result["score"],
        "total_questions": eval_result["total_questions"],
        "percentage": percentage,
        "passed": passed,
        "passing_score": PASSING_SCORE_THRESHOLD,
        "topic_performance": eval_result["topic_performance"],
        "weak_topics": eval_result["weak_topics"],
        "strengths": eval_result["strengths"],
        "recommended_revisions": eval_result["recommended_revisions"],
        "question_ids": [q["id"] for q in full_questions],
        "created_at": now_str
    }

    if db is not None:
        await db.phase_assessments.insert_one(attempt_doc)

    unlocked_next_phase = False
    next_phase_name = None

    if passed:
        # Check next phase to unlock
        p_num = target_phase["phase_number"]
        if p_num == 1:
            unlocked_next_phase = True
            next_phase_name = "Intermediate Phase"
        elif p_num == 2:
            unlocked_next_phase = True
            next_phase_name = "Advanced Phase"

    # Return refreshed roadmap
    refreshed_rm = await get_or_initialize_user_roadmap(user_id, roadmap["career_id"])

    message = (
        f"Congratulations! You passed {target_phase['name']} with {percentage}%! "
        + (f"{next_phase_name} is now UNLOCKED." if unlocked_next_phase else "You have successfully finished the entire roadmap!")
        if passed else
        f"Your score is {percentage}%. You need at least {PASSING_SCORE_THRESHOLD}% to complete this phase and unlock the next phase. Review the recommended lessons and try again."
    )

    return {
        "phase_id": phase_id,
        "phase_name": target_phase["name"],
        "score": eval_result["score"],
        "total_questions": eval_result["total_questions"],
        "percentage": percentage,
        "passed": passed,
        "passing_score": PASSING_SCORE_THRESHOLD,
        "unlocked_next_phase": unlocked_next_phase,
        "next_phase_name": next_phase_name,
        "weak_topics": eval_result["weak_topics"],
        "strengths": eval_result["strengths"],
        "recommended_revisions": eval_result["recommended_revisions"],
        "reviews": eval_result["reviews"],
        "message": message,
        "roadmap": refreshed_rm
    }

async def get_phase_assessment_history(user_id: str, phase_id: str) -> List[Dict[str, Any]]:
    """
    Returns full attempt history for a specific phase assessment for the authenticated student.
    """
    db = get_database()
    if db is not None:
        cursor = db.phase_assessments.find({"user_id": user_id, "phase_id": phase_id}).sort("created_at", -1)
        attempts = await cursor.to_list(length=50)
        for a in attempts:
            a["_id"] = str(a["_id"])
        return attempts
    return []
