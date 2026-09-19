import uuid
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from app.database.connection import get_database
from app.ml.recommendation_engine import load_careers_data, calculate_career_fit
from app.services.evidence_service import (
    get_or_create_user_evidence,
    get_verified_skills_dict,
    add_project_evidence
)

async def calculate_employability_for_verified_skills(
    user_id: str,
    career: Dict[str, Any],
    verified_skills: Dict[str, int]
) -> Dict[str, int]:
    db = get_database()
    profile = None
    if db is not None:
        profile = await db.student_profiles.find_one({"user_id": user_id})

    if not profile:
        profile = {
            "degree": "B.Tech",
            "interests": ["Artificial Intelligence", "Data Science"],
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

async def generate_adaptive_roadmap(user_id: str, career_id: str = "ai-engineer") -> Dict[str, Any]:
    db = get_database()
    now_str = datetime.now(timezone.utc).isoformat()

    careers = load_careers_data()
    career = next((c for c in careers if c["id"] == career_id), None)
    if not career:
        career = careers[0] if careers else {
            "id": "ai-engineer",
            "title": "AI Engineer",
            "required_skills": {"Python": 85, "Machine Learning": 80, "SQL": 75},
            "required_employability": 80
        }

    # Retrieve current verified skills & evidence
    evidence_data = await get_or_create_user_evidence(user_id)
    verified_map = {item["skill"]: item["verified_score"] for item in evidence_data["skills"]}
    confidence_map = {item["skill"]: item["confidence"] for item in evidence_data["skills"]}

    # Calculate Employability
    emp_metrics = await calculate_employability_for_verified_skills(user_id, career, verified_map)
    current_emp = emp_metrics["current_employability"]
    target_emp = emp_metrics["required_employability"]
    emp_gap = emp_metrics["employability_gap"]

    # Compute skill gaps for required skills
    required_skills = career.get("required_skills", {})
    skill_gaps = []
    for skill, req_val in required_skills.items():
        ver_val = verified_map.get(skill, 40)
        gap = max(0, req_val - ver_val)
        conf = confidence_map.get(skill, "LOW")

        priority = "LOW"
        if gap >= 30:
            priority = "HIGH"
        elif gap >= 15:
            priority = "MEDIUM"

        skill_gaps.append({
            "skill": skill,
            "required": req_val,
            "verified": ver_val,
            "gap": gap,
            "confidence": conf,
            "priority": priority
        })

    # Sort skills by gap descending (largest gap first)
    skill_gaps.sort(key=lambda x: x["gap"], reverse=True)

    roadmap_id = f"rm_{user_id}_{career['id']}"

    # Generate Phased Tasks
    phases = [
        "Phase 1: Core Fundamentals & Knowledge Acquisition",
        "Phase 2: Formal Assessment & Empirical Skill Verification",
        "Phase 3: Applied Project Development & Evidence Generation",
        "Phase 4: Secondary Skills & Technical Optimization",
        "Phase 5: Capstone Integration & Portfolio Deployment"
    ]

    tasks: List[Dict[str, Any]] = []

    # Has project evidence check
    has_projects = len(evidence_data.get("projects", [])) > 0

    # Phase 1: High-priority learning tasks
    high_gap_skills = [s for s in skill_gaps if s["priority"] == "HIGH"]
    med_gap_skills = [s for s in skill_gaps if s["priority"] == "MEDIUM"]
    low_gap_skills = [s for s in skill_gaps if s["priority"] == "LOW" and s["gap"] > 0]

    # If no high gap skills exist, promote the top skill
    if not high_gap_skills and skill_gaps:
        high_gap_skills = [skill_gaps[0]]

    for s in high_gap_skills:
        tasks.append({
            "id": f"task_{uuid.uuid4().hex[:8]}",
            "roadmap_id": roadmap_id,
            "user_id": user_id,
            "phase": 1,
            "phase_name": phases[0],
            "title": f"Learn {s['skill']} Fundamentals & Core Concepts",
            "description": f"Master foundational principles, architectures, and theoretical mechanics of {s['skill']}.",
            "skill": s["skill"],
            "type": "Learning",
            "priority": "HIGH",
            "estimated_effort": "8 hours",
            "status": "NOT STARTED",
            "explanation": f"Required Skill = {s['required']}, Verified Skill = {s['verified']}, Gap = {s['gap']} pts. High career impact for {career['title']}.",
            "completed_at": None
        })

    # Phase 2: Assessments for high-priority skills
    for s in high_gap_skills:
        tasks.append({
            "id": f"task_{uuid.uuid4().hex[:8]}",
            "roadmap_id": roadmap_id,
            "user_id": user_id,
            "phase": 2,
            "phase_name": phases[1],
            "title": f"Complete {s['skill']} Proficiency Assessment",
            "description": f"Take the timed technical assessment to benchmark objective competency in {s['skill']}.",
            "skill": s["skill"],
            "type": "Assessment",
            "priority": "HIGH",
            "estimated_effort": "2 hours",
            "status": "NOT STARTED",
            "explanation": f"Assessment evidence required to convert self-declared level into verified empirical score.",
            "completed_at": None
        })

    # Phase 3: Project building for primary skills
    for s in high_gap_skills:
        tasks.append({
            "id": f"task_{uuid.uuid4().hex[:8]}",
            "roadmap_id": roadmap_id,
            "user_id": user_id,
            "phase": 3,
            "phase_name": phases[2],
            "title": f"Build {s['skill']} Applied Project",
            "description": f"Develop a functional, production-ready module demonstrating real-world problem solving with {s['skill']}.",
            "skill": s["skill"],
            "type": "Project",
            "priority": "HIGH",
            "estimated_effort": "15 hours",
            "status": "NOT STARTED",
            "explanation": f"Practical project evidence contributes 40% weight toward full skill verification.",
            "completed_at": None
        })

    # Phase 4: Medium gap skills learning and practice
    for s in med_gap_skills:
        tasks.append({
            "id": f"task_{uuid.uuid4().hex[:8]}",
            "roadmap_id": roadmap_id,
            "user_id": user_id,
            "phase": 4,
            "phase_name": phases[3],
            "title": f"Improve {s['skill']} Practical Workflows",
            "description": f"Complete advanced algorithmic drills, schema optimizations, and integration scripts for {s['skill']}.",
            "skill": s["skill"],
            "type": "Practice",
            "priority": "MEDIUM",
            "estimated_effort": "6 hours",
            "status": "NOT STARTED",
            "explanation": f"Required Skill = {s['required']}, Current Verified = {s['verified']}, Gap = {s['gap']} pts.",
            "completed_at": None
        })

    # Phase 5: Final capstone evidence submission
    tasks.append({
        "id": f"task_{uuid.uuid4().hex[:8]}",
        "roadmap_id": roadmap_id,
        "user_id": user_id,
        "phase": 5,
        "phase_name": phases[4],
        "title": f"Deploy {career['title']} Capstone Portfolio Project",
        "description": f"Submit comprehensive GitHub repository and live deployment URL verifying multi-skill mastery.",
        "skill": high_gap_skills[0]["skill"] if high_gap_skills else "General",
        "type": "Evidence Submission",
        "priority": "HIGH" if not has_projects else "MEDIUM",
        "estimated_effort": "12 hours",
        "status": "NOT STARTED",
        "explanation": "Verified project evidence provides external validation for overall career achievability.",
        "completed_at": None
    })

    roadmap_doc = {
        "id": roadmap_id,
        "user_id": user_id,
        "career_id": career["id"],
        "career_title": career["title"],
        "target_employability": target_emp,
        "current_employability": current_emp,
        "employability_gap": emp_gap,
        "total_tasks": len(tasks),
        "completed_tasks": 0,
        "progress_percentage": 0,
        "phases": phases,
        "last_updated": now_str
    }

    if db is not None:
        await db.roadmaps.update_one(
            {"user_id": user_id},
            {"$set": roadmap_doc},
            upsert=True
        )
        # Clear existing tasks and insert new personalized tasks
        await db.roadmap_tasks.delete_many({"user_id": user_id})
        if tasks:
            # Insert copy so tasks list doesn't have BSON ObjectId
            insert_tasks = [{**t} for t in tasks]
            await db.roadmap_tasks.insert_many(insert_tasks)

    # Initialize employability history baseline if empty
    if db is not None:
        history_count = await db.employability_history.count_documents({"user_id": user_id})
        if history_count == 0:
            initial_history = [
                {
                    "user_id": user_id,
                    "date": "Week 1",
                    "score": max(35, current_emp - 6),
                    "career_id": career["id"],
                    "milestone": "Baseline Assessment",
                    "timestamp": now_str
                },
                {
                    "user_id": user_id,
                    "date": "Current",
                    "score": current_emp,
                    "career_id": career["id"],
                    "milestone": "Roadmap Generation",
                    "timestamp": now_str
                }
            ]
            await db.employability_history.insert_many(initial_history)

    cleaned_tasks = [{k: v for k, v in t.items() if k != "_id"} for t in tasks]

    return {
        **roadmap_doc,
        "tasks": cleaned_tasks
    }

async def get_user_roadmap(user_id: str) -> Dict[str, Any]:
    db = get_database()
    if db is not None:
        roadmap = await db.roadmaps.find_one({"user_id": user_id})
        if roadmap:
            cursor = db.roadmap_tasks.find({"user_id": user_id}).sort("phase", 1)
            tasks = await cursor.to_list(length=100)
            formatted_tasks = []
            completed_count = 0
            for t in tasks:
                t_dict = {
                    "id": t.get("id", str(t.get("_id"))),
                    "roadmap_id": t.get("roadmap_id", roadmap["id"]),
                    "phase": t.get("phase", 1),
                    "phase_name": t.get("phase_name", "Phase 1"),
                    "title": t.get("title", ""),
                    "description": t.get("description", ""),
                    "skill": t.get("skill", ""),
                    "type": t.get("type", "Learning"),
                    "priority": t.get("priority", "MEDIUM"),
                    "estimated_effort": t.get("estimated_effort", "4 hours"),
                    "status": t.get("status", "NOT STARTED"),
                    "explanation": t.get("explanation", ""),
                    "completed_at": t.get("completed_at")
                }
                if t_dict["status"] == "COMPLETED":
                    completed_count += 1
                formatted_tasks.append(t_dict)

            total = len(formatted_tasks)
            pct = int((completed_count / total * 100)) if total > 0 else 0

            return {
                "id": roadmap.get("id", f"rm_{user_id}"),
                "user_id": user_id,
                "career_id": roadmap.get("career_id", "ai-engineer"),
                "career_title": roadmap.get("career_title", "AI Engineer"),
                "target_employability": roadmap.get("target_employability", 80),
                "current_employability": roadmap.get("current_employability", 58),
                "employability_gap": roadmap.get("employability_gap", 22),
                "total_tasks": total,
                "completed_tasks": completed_count,
                "progress_percentage": pct,
                "phases": roadmap.get("phases", []),
                "tasks": formatted_tasks,
                "last_updated": roadmap.get("last_updated", "")
            }

    # Generate default roadmap if none found
    return await generate_adaptive_roadmap(user_id, "ai-engineer")

async def update_task_status(user_id: str, task_id: str, new_status: str) -> Dict[str, Any]:
    db = get_database()
    now_str = datetime.now(timezone.utc).isoformat()
    update_data = {"status": new_status}
    if new_status == "COMPLETED":
        update_data["completed_at"] = now_str

    if db is not None:
        await db.roadmap_tasks.update_one(
            {"user_id": user_id, "id": task_id},
            {"$set": update_data}
        )
    return await get_user_roadmap(user_id)

async def complete_task_and_recalculate(user_id: str, task_id: str) -> Dict[str, Any]:
    db = get_database()
    now_str = datetime.now(timezone.utc).isoformat()

    # 1. Fetch task
    task = None
    if db is not None:
        task = await db.roadmap_tasks.find_one({"user_id": user_id, "id": task_id})

    if not task:
        return await get_user_roadmap(user_id)

    skill_name = task.get("skill")
    task_type = task.get("type")

    # 2. Mark task completed
    if db is not None:
        await db.roadmap_tasks.update_one(
            {"user_id": user_id, "id": task_id},
            {"$set": {"status": "COMPLETED", "completed_at": now_str}}
        )

    # 3. Apply Empirical Skill Improvement based on Task Type
    if skill_name and skill_name != "General":
        if task_type == "Assessment":
            # Boost assessment score for this skill by +22 points
            if db is not None:
                ass = await db.assessment_results.find_one({"user_id": user_id})
                skill_scores = ass.get("skill_scores", {}) if ass else {}
                old_sc = skill_scores.get(skill_name, 40)
                new_sc = min(95, old_sc + 22)
                skill_scores[skill_name] = new_sc
                await db.assessment_results.update_one(
                    {"user_id": user_id},
                    {"$set": {"skill_scores": skill_scores}},
                    upsert=True
                )
        elif task_type == "Project":
            # Add project evidence for this skill
            await add_project_evidence(user_id, {
                "title": f"{skill_name} Practical Application Project",
                "description": f"Completed hands-on milestone project demonstrating {skill_name} implementation.",
                "skills_used": [skill_name],
                "project_type": "Academic",
                "completion_status": "Completed",
                "github_link": f"https://github.com/student/{skill_name.lower().replace(' ', '-')}-project",
                "student_role": "Lead Developer"
            })
        elif task_type in ["Learning", "Practice", "Evidence Submission"]:
            # Boost student profile claimed/base proficiency if needed
            if db is not None:
                prof = await db.student_profiles.find_one({"user_id": user_id})
                tech_skills = prof.get("technical_skills", {}) if prof else {}
                curr_sk = tech_skills.get(skill_name, 50)
                tech_skills[skill_name] = min(95, curr_sk + 10)
                await db.student_profiles.update_one(
                    {"user_id": user_id},
                    {"$set": {"technical_skills": tech_skills}}
                )

    # 4. Trigger Evidence Engine recalculation
    evidence_res = await get_or_create_user_evidence(user_id)
    verified_map = {item["skill"]: item["verified_score"] for item in evidence_res["skills"]}

    # 5. Recalculate Career Employability
    roadmap_info = await db.roadmaps.find_one({"user_id": user_id}) if db is not None else None
    career_id = roadmap_info.get("career_id", "ai-engineer") if roadmap_info else "ai-engineer"

    careers = load_careers_data()
    career = next((c for c in careers if c["id"] == career_id), None) or careers[0]

    emp_metrics = await calculate_employability_for_verified_skills(user_id, career, verified_map)
    new_emp = emp_metrics["current_employability"]
    new_gap = emp_metrics["employability_gap"]

    # 6. Append to employability_history
    if db is not None:
        hist_count = await db.employability_history.count_documents({"user_id": user_id})
        week_label = f"Week {hist_count + 1}"
        await db.employability_history.insert_one({
            "user_id": user_id,
            "date": week_label,
            "score": new_emp,
            "career_id": career["id"],
            "milestone": f"Completed: {task.get('title')}",
            "timestamp": now_str
        })

    # 7. Update skill_progress collection
    if db is not None and skill_name and skill_name != "General":
        ver_sc = verified_map.get(skill_name, 60)
        req_sc = career.get("required_skills", {}).get(skill_name, 80)
        gap_val = max(0, req_sc - ver_sc)

        await db.skill_progress.update_one(
            {"user_id": user_id, "skill": skill_name},
            {
                "$set": {
                    "current_score": ver_sc,
                    "target_score": req_sc,
                    "gap": gap_val,
                    "last_action": task.get("title"),
                    "updated_at": now_str
                },
                "$setOnInsert": {
                    "user_id": user_id,
                    "skill": skill_name,
                    "initial_score": max(20, ver_sc - 22)
                },
                "$push": {
                    "history": {
                        "date": now_str[:10],
                        "score": ver_sc,
                        "action": f"Completed {task.get('title')}"
                    }
                }
            },
            upsert=True
        )

    # 8. Adaptive Roadmap Prioritization:
    # Recalculate priorities of remaining uncompleted tasks based on updated skill gaps!
    if db is not None:
        uncompleted = await db.roadmap_tasks.find({"user_id": user_id, "status": {"$ne": "COMPLETED"}}).to_list(length=100)
        for t in uncompleted:
            t_skill = t.get("skill")
            if t_skill in career.get("required_skills", {}):
                req_val = career["required_skills"][t_skill]
                curr_ver = verified_map.get(t_skill, 50)
                curr_gap = max(0, req_val - curr_ver)

                # Dynamically adapt priority
                new_priority = "LOW"
                if curr_gap >= 30:
                    new_priority = "HIGH"
                elif curr_gap >= 15:
                    new_priority = "MEDIUM"

                new_explanation = f"Required = {req_val}, Current Verified = {curr_ver}, Gap = {curr_gap} pts. Priority adapted dynamically."

                await db.roadmap_tasks.update_one(
                    {"_id": t["_id"]},
                    {"$set": {
                        "priority": new_priority,
                        "explanation": new_explanation
                    }}
                )

        # Update roadmap document summary
        completed_tasks_count = await db.roadmap_tasks.count_documents({"user_id": user_id, "status": "COMPLETED"})
        total_tasks_count = await db.roadmap_tasks.count_documents({"user_id": user_id})
        pct = int((completed_tasks_count / total_tasks_count * 100)) if total_tasks_count > 0 else 0

        await db.roadmaps.update_one(
            {"user_id": user_id},
            {"$set": {
                "current_employability": new_emp,
                "employability_gap": new_gap,
                "completed_tasks": completed_tasks_count,
                "progress_percentage": pct,
                "last_updated": now_str
            }}
        )

    return await get_user_roadmap(user_id)
