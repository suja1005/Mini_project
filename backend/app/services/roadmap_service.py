import uuid
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from app.database.connection import get_database
from app.ml.recommendation_engine import load_careers_data, calculate_career_fit
from app.services.evidence_service import get_or_create_user_evidence, add_project_evidence
from app.services.question_generation_service import question_gen_service
from app.services.roadmap_curriculum import (
    CURRICULUM,
    get_all_skills,
    get_skill_curriculum,
    get_level_curriculum,
    get_all_curriculum_levels
)

async def calculate_employability_metrics(user_id: str, career: Dict[str, Any], verified_skills: Dict[str, int]) -> Dict[str, Any]:
    db = get_database()
    profile = None
    if db is not None:
        profile = await db.student_profiles.find_one({"user_id": user_id})
    if not profile:
        profile = {
            "degree": "B.Tech",
            "department": "Computer Science",
            "cgpa": "8.0",
            "aptitude_scores": {"logical_reasoning": 75, "numerical_ability": 70, "analytical_thinking": 80},
            "target_role": career.get("title", "AI Engineer")
        }

    temp_profile = {**profile, "technical_skills": verified_skills}
    fit_info = calculate_career_fit(temp_profile, career)
    fit_score = fit_info["fit_score"]

    tech_avg = sum(verified_skills.values()) / len(verified_skills) if verified_skills else 40
    apt_avg = sum(profile.get("aptitude_scores", {}).values()) / 3 if profile.get("aptitude_scores") else 70

    current_employability = int((fit_score * 0.50) + (tech_avg * 0.30) + (apt_avg * 0.20))
    current_employability = max(35, min(95, current_employability))
    required_employability = career.get("required_employability", 80)
    employability_gap = max(0, required_employability - current_employability)

    return {
        "fit_score": fit_score,
        "current_employability": current_employability,
        "required_employability": required_employability,
        "employability_gap": employability_gap
    }

async def init_user_skill_levels(user_id: str) -> List[Dict[str, Any]]:
    """
    Initializes all 21 levels (7 skills * 3 levels) for a user if not already initialized.
    Level 1 is set to AVAILABLE. Levels 2 and 3 are initially LOCKED.
    """
    db = get_database()
    all_levels_meta = get_all_curriculum_levels()

    if db is None:
        # Fallback memory structure
        initialized = []
        for lvl in all_levels_meta:
            status = "AVAILABLE" if lvl["level"] == 1 else "LOCKED"
            initialized.append({
                "id": f"{lvl['skill_slug']}_lvl_{lvl['level']}",
                "user_id": user_id,
                "skill": lvl["skill"],
                "skill_slug": lvl["skill_slug"],
                "level": lvl["level"],
                "title": lvl["title"],
                "status": status,
                "learning_progress_percentage": 0,
                "assessment_status": "NOT_STARTED",
                "quiz_score": None,
                "attempts_count": 0,
                "topics_progress": {},
                "passed": False,
                "completed_at": None
            })
        return initialized

    cursor = db.user_skill_levels.find({"user_id": user_id})
    existing = await cursor.to_list(length=100)
    existing_map = {doc.get("level_id", doc.get("id")): doc for doc in existing}

    docs_to_insert = []
    for lvl in all_levels_meta:
        lvl_id = f"{lvl['skill_slug']}_lvl_{lvl['level']}"
        if lvl_id not in existing_map:
            status = "AVAILABLE" if lvl["level"] == 1 else "LOCKED"
            new_doc = {
                "id": lvl_id,
                "level_id": lvl_id,
                "user_id": user_id,
                "skill": lvl["skill"],
                "skill_slug": lvl["skill_slug"],
                "level": lvl["level"],
                "title": lvl["title"],
                "status": status,
                "learning_progress_percentage": 0,
                "assessment_status": "NOT_STARTED",
                "quiz_score": None,
                "attempts_count": 0,
                "topics_progress": {},
                "passed": False,
                "completed_at": None,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            docs_to_insert.append(new_doc)
            existing_map[lvl_id] = new_doc

    if docs_to_insert:
        await db.user_skill_levels.insert_many(docs_to_insert)

    return list(existing_map.values())

async def get_skills_overview(user_id: str) -> List[Dict[str, Any]]:
    """
    Returns the 7 skills overview with user progression across all 3 levels.
    """
    db = get_database()
    await init_user_skill_levels(user_id)

    user_levels_docs = []
    if db is not None:
        cursor = db.user_skill_levels.find({"user_id": user_id})
        user_levels_docs = await cursor.to_list(length=100)

    user_level_map = {doc.get("level_id", doc.get("id")): doc for doc in user_levels_docs}

    all_skills_meta = get_all_skills()
    skills_response = []

    for s in all_skills_meta:
        slug = s["skill_slug"]
        curric = get_skill_curriculum(slug) or {}
        levels_curric = curric.get("levels", [])

        skill_levels_list = []
        passed_levels_count = 0
        total_topics_count = 0
        completed_topics_count = 0

        for lvl_c in levels_curric:
            lvl_num = lvl_c["level"]
            lvl_id = f"{slug}_lvl_{lvl_num}"
            u_doc = user_level_map.get(lvl_id, {})

            status = u_doc.get("status", "LOCKED" if lvl_num > 1 else "AVAILABLE")
            passed = u_doc.get("passed", False) or (status == "PASSED")
            if passed:
                passed_levels_count += 1
                status = "PASSED"

            # Enforce sequential prerequisites strictly
            if lvl_num == 2 and status != "PASSED":
                lvl1_id = f"{slug}_lvl_1"
                lvl1_passed = user_level_map.get(lvl1_id, {}).get("passed", False) or (user_level_map.get(lvl1_id, {}).get("status") == "PASSED")
                if not lvl1_passed:
                    status = "LOCKED"
                elif status == "LOCKED":
                    status = "AVAILABLE"

            if lvl_num == 3 and status != "PASSED":
                lvl2_id = f"{slug}_lvl_2"
                lvl2_passed = user_level_map.get(lvl2_id, {}).get("passed", False) or (user_level_map.get(lvl2_id, {}).get("status") == "PASSED")
                if not lvl2_passed:
                    status = "LOCKED"
                elif status == "LOCKED":
                    status = "AVAILABLE"

            topics_progress = u_doc.get("topics_progress", {})
            topics = lvl_c.get("topics", [])
            total_topics_count += len(topics)

            # Build enriched topic list
            lvl_topics = []
            lvl_done = 0
            for idx, top in enumerate(topics):
                top_id = f"{slug}_l{lvl_num}_top_{idx+1:02d}"
                t_state = topics_progress.get(top_id, {})
                t_comp = t_state.get("completed", False)
                p_comp = t_state.get("practice_completed", False)

                if t_comp and p_comp:
                    lvl_done += 1
                    completed_topics_count += 1

                lvl_topics.append({
                    "id": top_id,
                    "title": top[0],
                    "estimated_hours": top[1],
                    "description": top[2],
                    "practical_example": top[3],
                    "practice_task": {
                        "id": f"{top_id}_pt",
                        "title": f"Practice: {top[0]}",
                        "instructions": top[4],
                        "hint": top[5],
                        "completed": p_comp
                    },
                    "completed": t_comp,
                    "practice_completed": p_comp,
                    "resources": [
                        {"title": f"{top[0]} Reference", "type": "Documentation", "url": "https://docs.python.org/3/", "provider": "Official"}
                    ],
                    "subtopics": []
                })

            pct = int(round((lvl_done / len(topics)) * 100)) if topics else 0
            if passed:
                pct = 100

            skill_levels_list.append({
                "id": lvl_id,
                "skill": s["skill"],
                "skill_slug": slug,
                "level": lvl_num,
                "level_name": lvl_c.get("title", f"Level {lvl_num}"),
                "title": lvl_c.get("title", f"Level {lvl_num}"),
                "description": lvl_c.get("description", ""),
                "difficulty": lvl_c.get("difficulty", "Beginner"),
                "estimated_hours": lvl_c.get("estimated_hours", "20 hours"),
                "learning_objectives": lvl_c.get("learning_objectives", []),
                "topics": lvl_topics,
                "prerequisites": [f"{slug}_lvl_{lvl_num-1}"] if lvl_num > 1 else [],
                "status": status,
                "learning_progress_percentage": pct,
                "assessment_status": "PASSED" if passed else u_doc.get("assessment_status", "NOT_STARTED"),
                "quiz_score": u_doc.get("quiz_score"),
                "attempts_count": u_doc.get("attempts_count", 0),
                "passing_score": 70,
                "time_limit_minutes": 30 + (lvl_num * 5),
                "completed_at": u_doc.get("completed_at")
            })

        # Calculate skill overall completion percentage
        skill_pct = int(round((passed_levels_count / 3) * 100))
        current_lvl_num = min(3, passed_levels_count + 1)

        skills_response.append({
            "skill": s["skill"],
            "skill_slug": slug,
            "category": s["category"],
            "description": s["description"],
            "icon": s["icon"],
            "total_levels": 3,
            "passed_levels": passed_levels_count,
            "current_level": current_lvl_num,
            "progress_percentage": skill_pct,
            "total_learning_hours": f"{sum(int(lvl['estimated_hours'].split()[0]) for lvl in skill_levels_list)} hours",
            "levels": skill_levels_list
        })

    return skills_response

async def get_skill_level_detail(user_id: str, skill_slug: str, level_num: int) -> Dict[str, Any]:
    skills = await get_skills_overview(user_id)
    target_skill = next((s for s in skills if s["skill_slug"] == skill_slug.lower()), None)
    if not target_skill:
        raise ValueError(f"Skill '{skill_slug}' not found.")

    target_level = next((lvl for lvl in target_skill["levels"] if lvl["level"] == level_num), None)
    if not target_level:
        raise ValueError(f"Level {level_num} for skill '{skill_slug}' not found.")

    return target_level

async def start_skill_level(user_id: str, skill_slug: str, level_num: int) -> Dict[str, Any]:
    db = get_database()
    level_detail = await get_skill_level_detail(user_id, skill_slug, level_num)

    # Progression validation
    if level_detail["status"] == "LOCKED":
        prereq = f"Level {level_num - 1}"
        raise ValueError(f"Cannot start Level {level_num}. You must complete all topics and pass the assessment for {prereq} first.")

    level_id = f"{skill_slug}_lvl_{level_num}"
    new_status = "IN_PROGRESS" if level_detail["status"] in ["AVAILABLE", "NEEDS_REVISION"] else level_detail["status"]

    if db is not None:
        await db.user_skill_levels.update_one(
            {"user_id": user_id, "id": level_id},
            {"$set": {"status": new_status}},
            upsert=True
        )

    return await get_skill_level_detail(user_id, skill_slug, level_num)

async def toggle_level_topic(
    user_id: str,
    skill_slug: str,
    level_num: int,
    topic_id: str,
    completed: Optional[bool] = None,
    practice_completed: Optional[bool] = None
) -> Dict[str, Any]:
    db = get_database()
    level_detail = await get_skill_level_detail(user_id, skill_slug, level_num)

    if level_detail["status"] == "LOCKED":
        raise ValueError("Cannot modify topics in a locked level.")

    level_id = f"{skill_slug}_lvl_{level_num}"
    user_doc = None
    if db is not None:
        user_doc = await db.user_skill_levels.find_one({"user_id": user_id, "id": level_id})

    topics_progress = user_doc.get("topics_progress", {}) if user_doc else {}
    t_state = topics_progress.setdefault(topic_id, {"completed": False, "practice_completed": False})

    if completed is not None:
        t_state["completed"] = completed
    if practice_completed is not None:
        t_state["practice_completed"] = practice_completed

    # Tally overall progress for level
    topics = level_detail.get("topics", [])
    total_topics = len(topics)
    completed_both = 0

    for top in topics:
        t_id = top["id"]
        st = topics_progress.get(t_id, {})
        if st.get("completed", False) and st.get("practice_completed", False):
            completed_both += 1

    pct = int(round((completed_both / total_topics) * 100)) if total_topics > 0 else 0

    curr_status = level_detail["status"]
    if pct == 100:
        if curr_status not in ["PASSED"]:
            curr_status = "ASSESSMENT_PENDING"
    elif curr_status not in ["PASSED", "NEEDS_REVISION"]:
        curr_status = "IN_PROGRESS"

    if db is not None:
        await db.user_skill_levels.update_one(
            {"user_id": user_id, "id": level_id},
            {"$set": {
                "topics_progress": topics_progress,
                "learning_progress_percentage": pct,
                "status": curr_status
            }},
            upsert=True
        )

    return await get_skill_level_detail(user_id, skill_slug, level_num)

async def generate_level_assessment(user_id: str, skill_slug: str, level_num: int) -> Dict[str, Any]:
    db = get_database()
    level_detail = await get_skill_level_detail(user_id, skill_slug, level_num)

    if level_detail["status"] == "LOCKED":
        raise ValueError(f"Cannot take assessment for locked level {level_num}.")

    level_id = f"{skill_slug}_lvl_{level_num}"
    skill_name = level_detail["skill"]

    # Gather past question IDs to guarantee non-repeating retakes
    used_ids = []
    if db is not None:
        cursor = db.roadmap_verifications.find({"user_id": user_id, "level_id": level_id})
        past_attempts = await cursor.to_list(length=50)
        for att in past_attempts:
            used_ids.extend(att.get("question_ids", []))

    # Generate 20 questions (15 MCQ + 5 Practical)
    client_qs, full_qs = question_gen_service.generate_level_assessment(
        skill=skill_name,
        level=level_num,
        topics=level_detail.get("topics", []),
        exclude_ids=used_ids,
        mcq_count=15,
        practical_count=5
    )

    time_limit = level_detail.get("time_limit_minutes", 30)

    # Store full questions securely in db.active_quizzes
    if db is not None:
        await db.active_quizzes.update_one(
            {"user_id": user_id, "level_id": level_id},
            {"$set": {
                "user_id": user_id,
                "level_id": level_id,
                "skill": skill_name,
                "skill_slug": skill_slug,
                "level": level_num,
                "full_questions": full_qs,
                "time_limit_minutes": time_limit,
                "created_at": datetime.now(timezone.utc).isoformat()
            }},
            upsert=True
        )

    return {
        "level_id": level_id,
        "skill": skill_name,
        "level": level_num,
        "total_questions": len(client_qs),
        "time_limit_minutes": time_limit,
        "questions": client_qs
    }

async def submit_level_assessment(
    user_id: str,
    skill_slug: str,
    level_num: int,
    answers: Dict[str, str]
) -> Dict[str, Any]:
    db = get_database()
    now_str = datetime.now(timezone.utc).isoformat()
    level_id = f"{skill_slug}_lvl_{level_num}"
    level_detail = await get_skill_level_detail(user_id, skill_slug, level_num)

    active_quiz = None
    if db is not None:
        active_quiz = await db.active_quizzes.find_one({"user_id": user_id, "level_id": level_id})

    full_questions = active_quiz.get("full_questions", []) if active_quiz else []
    if not full_questions:
        # Fallback question generation if active quiz expired
        _, full_questions = question_gen_service.generate_level_assessment(
            skill=level_detail["skill"],
            level=level_num,
            topics=level_detail.get("topics", []),
            mcq_count=15,
            practical_count=5
        )

    # Evaluate answers on backend
    eval_result = question_gen_service.evaluate_assessment(
        full_questions=full_questions,
        student_answers=answers,
        passing_score=level_detail.get("passing_score", 70)
    )

    # Count attempts
    attempts_count = 1
    if db is not None:
        past_count = await db.roadmap_verifications.count_documents({"user_id": user_id, "level_id": level_id})
        attempts_count = past_count + 1

    question_ids = [q["id"] for q in full_questions]

    # Save attempt document
    attempt_doc = {
        "id": f"att_{uuid.uuid4().hex[:8]}",
        "user_id": user_id,
        "student_id": user_id, # for backwards compatibility
        "skill": level_detail["skill"],
        "skill_slug": skill_slug,
        "level": level_num,
        "level_id": level_id,
        "task_id": level_id, # for backwards compatibility
        "attempt_number": attempts_count,
        "score": eval_result["score"],
        "total_questions": eval_result["total_questions"],
        "percentage": eval_result["percentage"],
        "passed": eval_result["passed"],
        "topic_performance": eval_result["topic_performance"],
        "weak_topics": eval_result["weak_topics"],
        "strengths": eval_result["strengths"],
        "reviews": eval_result["reviews"],
        "question_ids": question_ids,
        "created_at": now_str
    }

    if db is not None:
        await db.roadmap_verifications.insert_one(attempt_doc)

    unlocked_next = False
    next_level_id = None
    new_status = "PASSED" if eval_result["passed"] else "NEEDS_REVISION"

    if db is not None:
        # Update current level status
        await db.user_skill_levels.update_one(
            {"user_id": user_id, "id": level_id},
            {"$set": {
                "status": new_status,
                "passed": eval_result["passed"],
                "quiz_score": eval_result["percentage"],
                "attempts_count": attempts_count,
                "assessment_status": "PASSED" if eval_result["passed"] else "FAILED",
                "completed_at": now_str if eval_result["passed"] else None
            }}
        )

        # Progression unlock on backend if passed!
        if eval_result["passed"] and level_num < 3:
            unlocked_next = True
            next_lvl_num = level_num + 1
            next_level_id = f"{skill_slug}_lvl_{next_lvl_num}"
            await db.user_skill_levels.update_one(
                {"user_id": user_id, "id": next_level_id},
                {"$set": {"status": "AVAILABLE"}},
                upsert=True
            )

        # Update evidence engine and employability metrics
        if eval_result["passed"]:
            skill_name = level_detail["skill"]
            # Upgrade evidence score
            target_score = 65 if level_num == 1 else (80 if level_num == 2 else 95)
            await db.skill_evidence.update_one(
                {"user_id": user_id, "skill": skill_name},
                {"$set": {
                    "verified_score": target_score,
                    "assessment_evidence": eval_result["percentage"],
                    "confidence": "HIGH",
                    "status": "VERIFIED",
                    "updated_at": now_str
                }},
                upsert=True
            )

            # Recalculate employability
            careers = load_careers_data()
            career = careers[0]
            evidence_res = await get_or_create_user_evidence(user_id)
            verified_map = {item["skill"]: item["verified_score"] for item in evidence_res.get("skills", [])}
            emp_metrics = await calculate_employability_metrics(user_id, career, verified_map)

            await db.roadmaps.update_one(
                {"user_id": user_id},
                {"$set": {
                    "current_employability": emp_metrics["current_employability"],
                    "employability_gap": emp_metrics["employability_gap"],
                    "last_updated": now_str
                }},
                upsert=True
            )

    msg = (
        f"Congratulations! You passed Level {level_num} with {eval_result['percentage']}%."
        if eval_result["passed"]
        else f"Score {eval_result['percentage']}% is below the 70% passing threshold. Review weak topics and retake the assessment."
    )

    return {
        "level_id": level_id,
        "skill": level_detail["skill"],
        "level": level_num,
        "score": eval_result["score"],
        "total_questions": eval_result["total_questions"],
        "percentage": eval_result["percentage"],
        "passed": eval_result["passed"],
        "status": new_status,
        "passing_score": 70,
        "attempts_count": attempts_count,
        "topic_performance": eval_result["topic_performance"],
        "strengths": eval_result["strengths"],
        "weak_topics": eval_result["weak_topics"],
        "recommended_revisions": eval_result["recommended_revisions"],
        "suggested_practice": eval_result["suggested_practice"],
        "reviews": eval_result["reviews"],
        "unlocked_next_level": unlocked_next,
        "next_level_id": next_level_id,
        "message": msg
    }

async def get_level_assessment_history(user_id: str, skill_slug: str, level_num: int) -> List[Dict[str, Any]]:
    db = get_database()
    level_id = f"{skill_slug}_lvl_{level_num}"
    history = []
    if db is not None:
        cursor = db.roadmap_verifications.find({"user_id": user_id, "level_id": level_id}).sort("attempt_number", 1)
        records = await cursor.to_list(length=100)
        for r in records:
            history.append({
                "id": str(r.get("_id", r.get("id"))),
                "level_id": r.get("level_id"),
                "task_id": r.get("task_id", level_id),
                "skill": r.get("skill"),
                "level": r.get("level", level_num),
                "student_id": r.get("user_id"),
                "attempt_number": r.get("attempt_number", 1),
                "score": r.get("score", 0),
                "total_questions": r.get("total_questions", 20),
                "percentage": r.get("percentage", 0),
                "passed": r.get("passed", False),
                "topic_performance": r.get("topic_performance", {}),
                "weak_topics": r.get("weak_topics", []),
                "strengths": r.get("strengths", []),
                "created_at": r.get("created_at", "")
            })
    return history

async def get_progress_dashboard(user_id: str) -> Dict[str, Any]:
    db = get_database()
    skills = await get_skills_overview(user_id)

    total_levels = 21
    passed_levels = 0
    in_prog_levels = 0
    locked_levels = 0
    needs_revision_levels = 0

    topics_completed = 0
    topics_remaining = 0
    total_hours_est = 0.0
    total_hours_comp = 0.0

    all_scores = []
    total_attempts = 0
    weak_topics_agg = {}

    recommended_next = None

    for s in skills:
        for lvl in s["levels"]:
            st = lvl["status"]
            hours_val = float(lvl["estimated_hours"].split()[0])
            total_hours_est += hours_val

            if st == "PASSED":
                passed_levels += 1
                total_hours_comp += hours_val
            elif st == "IN_PROGRESS":
                in_prog_levels += 1
                total_hours_comp += (hours_val * (lvl["learning_progress_percentage"] / 100))
                if not recommended_next:
                    recommended_next = {
                        "skill": s["skill"],
                        "skill_slug": s["skill_slug"],
                        "level": lvl["level"],
                        "title": lvl["title"],
                        "action": "Continue Learning Topics"
                    }
            elif st == "ASSESSMENT_PENDING":
                in_prog_levels += 1
                total_hours_comp += hours_val
                if not recommended_next:
                    recommended_next = {
                        "skill": s["skill"],
                        "skill_slug": s["skill_slug"],
                        "level": lvl["level"],
                        "title": lvl["title"],
                        "action": "Take Level Assessment"
                    }
            elif st == "NEEDS_REVISION":
                needs_revision_levels += 1
                total_hours_comp += (hours_val * 0.8)
                if not recommended_next:
                    recommended_next = {
                        "skill": s["skill"],
                        "skill_slug": s["skill_slug"],
                        "level": lvl["level"],
                        "title": lvl["title"],
                        "action": "Review Weak Topics & Retake Assessment"
                    }
            elif st == "LOCKED":
                locked_levels += 1
            elif st == "AVAILABLE":
                if not recommended_next:
                    recommended_next = {
                        "skill": s["skill"],
                        "skill_slug": s["skill_slug"],
                        "level": lvl["level"],
                        "title": lvl["title"],
                        "action": "Start Level 1"
                    }

            if lvl["quiz_score"] is not None:
                all_scores.append(lvl["quiz_score"])
            total_attempts += lvl["attempts_count"]

            for top in lvl.get("topics", []):
                if top.get("completed") and top.get("practice_completed"):
                    topics_completed += 1
                else:
                    topics_remaining += 1

    # Fetch recent weak topics from verifications
    if db is not None:
        cursor = db.roadmap_verifications.find({"user_id": user_id, "passed": False})
        failed_attempts = await cursor.to_list(length=50)
        for fa in failed_attempts:
            for wt in fa.get("weak_topics", []):
                weak_topics_agg[wt] = weak_topics_agg.get(wt, 0) + 1

    weak_topics_list = [
        {"topic": k, "fail_frequency": v, "recommendation": f"Dedicate focused study to master '{k}'."}
        for k, v in sorted(weak_topics_agg.items(), key=lambda item: item[1], reverse=True)
    ]

    overall_pct = int(round((passed_levels / total_levels) * 100)) if total_levels > 0 else 0
    avg_score = int(round(sum(all_scores) / len(all_scores))) if all_scores else 0

    return {
        "user_id": user_id,
        "career_title": "AI Engineer",
        "overall_completion_percentage": overall_pct,
        "skills_progress": skills,
        "levels_progress": {
            "passed": passed_levels,
            "in_progress": in_prog_levels,
            "locked": locked_levels,
            "needs_revision": needs_revision_levels
        },
        "topics_completed": topics_completed,
        "topics_remaining": topics_remaining,
        "total_learning_hours_completed": round(total_hours_comp, 1),
        "total_learning_hours_estimated": round(total_hours_est, 1),
        "assessment_attempts_total": total_attempts,
        "assessment_average_score": avg_score,
        "passed_levels_count": passed_levels,
        "total_levels_count": total_levels,
        "recommended_next_step": recommended_next or {
            "skill": "Python",
            "skill_slug": "python",
            "level": 1,
            "title": "Level 1 – Beginner",
            "action": "Begin Learning"
        },
        "weak_topics_to_revise": weak_topics_list[:8]
    }

# ==============================================================================
# Legacy Functions for Full Backward Compatibility
# ==============================================================================

async def get_user_roadmap(user_id: str) -> Dict[str, Any]:
    skills = await get_skills_overview(user_id)
    dashboard = await get_progress_dashboard(user_id)

    db = get_database()
    roadmap_meta = await db.roadmaps.find_one({"user_id": user_id}) if db is not None else None
    now_str = datetime.now(timezone.utc).isoformat()

    tasks = []
    order = 1
    for s in skills:
        for lvl in s["levels"]:
            tasks.append({
                "id": lvl["id"],
                "roadmap_id": f"rm_{user_id}",
                "phase": lvl["level"],
                "phase_name": f"{s['skill']} - {lvl['level_name']}",
                "title": f"{s['skill']} {lvl['title']}",
                "description": lvl["description"],
                "difficulty": lvl["difficulty"],
                "estimated_hours": lvl["estimated_hours"],
                "priority": "HIGH" if lvl["level"] == 1 else "MEDIUM",
                "status": "VERIFIED" if lvl["status"] == "PASSED" else ("LOCKED" if lvl["status"] == "LOCKED" else "NOT_STARTED"),
                "order": order,
                "prerequisites": lvl["prerequisites"],
                "skill": s["skill"],
                "type": "Learning",
                "explanation": f"Master {s['skill']} at {lvl['title']} standard.",
                "passing_score": 70,
                "verification_status": "Verified" if lvl["status"] == "PASSED" else "Not Started",
                "quiz_score": lvl["quiz_score"],
                "attempts_count": lvl["attempts_count"],
                "learning_progress_percentage": lvl["learning_progress_percentage"],
                "learning_objectives": lvl["learning_objectives"],
                "topics": lvl["topics"],
                "resources": [],
                "completed_at": lvl["completed_at"]
            })
            order += 1

    return {
        "id": f"rm_{user_id}",
        "user_id": user_id,
        "career_id": roadmap_meta.get("career_id", "ai-engineer") if roadmap_meta else "ai-engineer",
        "career_title": roadmap_meta.get("career_title", "AI Engineer") if roadmap_meta else "AI Engineer",
        "target_employability": roadmap_meta.get("target_employability", 80) if roadmap_meta else 80,
        "current_employability": roadmap_meta.get("current_employability", 60) if roadmap_meta else 60,
        "employability_gap": roadmap_meta.get("employability_gap", 20) if roadmap_meta else 20,
        "total_tasks": len(tasks),
        "verified_tasks": dashboard["passed_levels_count"],
        "completed_tasks": dashboard["passed_levels_count"],
        "progress_percentage": dashboard["overall_completion_percentage"],
        "phases": ["Beginner Fundamentals", "Intermediate Practice", "Advanced Production"],
        "tasks": tasks,
        "skills": skills,
        "last_updated": now_str
    }

async def generate_adaptive_roadmap(user_id: str, career_id: str = "ai-engineer") -> Dict[str, Any]:
    await init_user_skill_levels(user_id)
    return await get_user_roadmap(user_id)

async def get_task_by_id(user_id: str, task_id: str) -> Optional[Dict[str, Any]]:
    roadmap = await get_user_roadmap(user_id)
    return next((t for t in roadmap.get("tasks", []) if t["id"] == task_id), None)

async def start_task(user_id: str, task_id: str) -> Dict[str, Any]:
    # Extract skill and level from task_id (e.g. python_lvl_1)
    parts = task_id.split("_lvl_")
    if len(parts) == 2:
        skill_slug = parts[0]
        level_num = int(parts[1])
        await start_skill_level(user_id, skill_slug, level_num)
    return await get_user_roadmap(user_id)

async def toggle_subtopic(user_id: str, task_id: str, topic_id: str, subtopic_id: str, completed: bool) -> Dict[str, Any]:
    parts = task_id.split("_lvl_")
    if len(parts) == 2:
        skill_slug = parts[0]
        level_num = int(parts[1])
        await toggle_level_topic(user_id, skill_slug, level_num, topic_id, completed=completed)
    return await get_user_roadmap(user_id)

async def complete_learning(user_id: str, task_id: str) -> Dict[str, Any]:
    parts = task_id.split("_lvl_")
    if len(parts) == 2:
        skill_slug = parts[0]
        level_num = int(parts[1])
        level_detail = await get_skill_level_detail(user_id, skill_slug, level_num)
        for top in level_detail.get("topics", []):
            await toggle_level_topic(user_id, skill_slug, level_num, top["id"], completed=True, practice_completed=True)
    return await get_user_roadmap(user_id)

async def generate_task_questions(user_id: str, task_id: str) -> List[Dict[str, Any]]:
    parts = task_id.split("_lvl_")
    skill_slug = parts[0] if len(parts) == 2 else "python"
    level_num = int(parts[1]) if len(parts) == 2 else 1
    res = await generate_level_assessment(user_id, skill_slug, level_num)
    return res["questions"]

async def submit_task_verification(user_id: str, task_id: str, answers: Dict[str, str]) -> Dict[str, Any]:
    parts = task_id.split("_lvl_")
    skill_slug = parts[0] if len(parts) == 2 else "python"
    level_num = int(parts[1]) if len(parts) == 2 else 1
    res = await submit_level_assessment(user_id, skill_slug, level_num, answers)
    legacy_topic_perf = {k: v["percentage"] for k, v in res["topic_performance"].items()}
    return {
        "task_id": task_id,
        "score": res["score"],
        "total_questions": res["total_questions"],
        "percentage": res["percentage"],
        "passed": res["passed"],
        "status": res["status"],
        "topic_performance": legacy_topic_perf,
        "weak_topics": res["weak_topics"],
        "message": res["message"],
        "unlocked_next_task": res["unlocked_next_level"],
        "attempts_count": res["attempts_count"]
    }

async def get_verification_history(user_id: str, task_id: str) -> List[Dict[str, Any]]:
    parts = task_id.split("_lvl_")
    skill_slug = parts[0] if len(parts) == 2 else "python"
    level_num = int(parts[1]) if len(parts) == 2 else 1
    return await get_level_assessment_history(user_id, skill_slug, level_num)
