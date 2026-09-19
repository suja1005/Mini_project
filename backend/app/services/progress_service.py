from datetime import datetime, timezone
from typing import Dict, List, Any
from app.database.connection import get_database
from app.services.roadmap_service import get_user_roadmap
from app.services.evidence_service import get_or_create_user_evidence
from app.ml.recommendation_engine import load_careers_data

async def get_progress_overview(user_id: str) -> Dict[str, Any]:
    db = get_database()
    now_str = datetime.now(timezone.utc).isoformat()

    # 1. Active roadmap
    roadmap = await get_user_roadmap(user_id)
    career_title = roadmap.get("career_title", "AI Engineer")
    career_id = roadmap.get("career_id", "ai-engineer")
    current_emp = roadmap.get("current_employability", 58)
    target_emp = roadmap.get("target_employability", 80)
    emp_gap = roadmap.get("employability_gap", 22)
    completed_count = roadmap.get("completed_tasks", 0)
    total_count = roadmap.get("total_tasks", 1)

    # 2. History points
    history_points = []
    if db is not None:
        cursor = db.employability_history.find({"user_id": user_id}).sort("timestamp", 1)
        history_points = await cursor.to_list(length=50)

    if not history_points:
        history_points = [
            {"date": "Week 1", "score": 52, "milestone": "Initial Profile Setup", "timestamp": now_str},
            {"date": "Week 2", "score": 58, "milestone": "Aptitude Assessment", "timestamp": now_str},
            {"date": "Current", "score": current_emp, "milestone": "Roadmap Activated", "timestamp": now_str}
        ]

    formatted_history = []
    for h in history_points:
        formatted_history.append({
            "date": h.get("date", "Week 1"),
            "score": h.get("score", 50),
            "milestone": h.get("milestone", "Milestone"),
            "timestamp": h.get("timestamp", now_str)
        })

    # Previous score
    if len(formatted_history) >= 2:
        previous_emp = formatted_history[-2]["score"]
    else:
        previous_emp = max(35, current_emp - 6)

    improvement_delta = current_emp - previous_emp

    # 3. Evidence Engine summary
    evidence_res = await get_or_create_user_evidence(user_id)
    verified_map = {item["skill"]: item["verified_score"] for item in evidence_res["skills"]}

    # 4. Skill Progress
    careers = load_careers_data()
    career = next((c for c in careers if c["id"] == career_id), None) or careers[0]
    required_skills = career.get("required_skills", {"Python": 85, "Machine Learning": 80, "SQL": 75})

    skill_progress_items = []
    for skill, req_sc in required_skills.items():
        curr_sc = verified_map.get(skill, 40)
        
        # Check if saved in db.skill_progress
        sp_doc = None
        if db is not None:
            sp_doc = await db.skill_progress.find_one({"user_id": user_id, "skill": skill})

        init_sc = sp_doc.get("initial_score") if sp_doc else max(25, curr_sc - 15)
        gap_sc = max(0, req_sc - curr_sc)
        delta_sc = curr_sc - init_sc

        status = "ACHIEVED" if gap_sc == 0 else ("ON_TRACK" if delta_sc > 0 else "NEEDS_ATTENTION")

        skill_progress_items.append({
            "skill": skill,
            "initial_score": init_sc,
            "current_score": curr_sc,
            "target_score": req_sc,
            "gap": gap_sc,
            "improvement": delta_sc,
            "status": status
        })

    task_rate = int((completed_count / total_count * 100)) if total_count > 0 else 0

    return {
        "user_id": user_id,
        "target_career": career_title,
        "current_employability": current_emp,
        "previous_employability": previous_emp,
        "target_employability": target_emp,
        "employability_gap": emp_gap,
        "improvement_delta": improvement_delta,
        "completed_tasks_count": completed_count,
        "total_tasks_count": total_count,
        "task_completion_rate": task_rate,
        "verified_skills_count": evidence_res.get("total_verified", 0),
        "partial_skills_count": evidence_res.get("total_partially_verified", 0),
        "history": formatted_history,
        "skill_progress": skill_progress_items
    }

async def get_skill_progress_list(user_id: str) -> List[Dict[str, Any]]:
    overview = await get_progress_overview(user_id)
    return overview.get("skill_progress", [])

async def get_employability_progress_data(user_id: str) -> Dict[str, Any]:
    overview = await get_progress_overview(user_id)
    delta = overview["improvement_delta"]
    status_label = "Improving" if delta > 0 else ("Steady" if delta == 0 else "Needs Action")
    return {
        "current_employability": overview["current_employability"],
        "previous_employability": overview["previous_employability"],
        "target_employability": overview["target_employability"],
        "employability_gap": overview["employability_gap"],
        "improvement_delta": delta,
        "status": status_label
    }

async def get_employability_history_list(user_id: str) -> List[Dict[str, Any]]:
    overview = await get_progress_overview(user_id)
    return overview.get("history", [])
