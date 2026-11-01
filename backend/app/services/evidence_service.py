from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from bson import ObjectId
from app.database.connection import get_database

def score_to_level(score: int) -> str:
    if score >= 80:
        return "Advanced"
    elif score >= 50:
        return "Intermediate"
    return "Beginner"

def level_to_score(level: str) -> int:
    lvl = level.lower()
    if "adv" in lvl:
        return 85
    elif "inter" in lvl:
        return 60
    return 30

def calculate_project_score(project: Dict[str, Any]) -> int:
    score = 80 if project.get("completion_status") == "Completed" else 55
    if project.get("github_link"):
        score += 5
    if project.get("project_link"):
        score += 5
    return min(95, score)

def compute_evidence_for_skill(
    skill: str,
    claimed_score: int,
    assessment_score: Optional[int],
    project_score: Optional[int]
) -> Dict[str, Any]:
    notes = []
    claimed_level = score_to_level(claimed_score)

    if assessment_score is not None and project_score is not None:
        # Transparent academic formula: Assessment 60% + Project 40%
        verified_score = int(round((assessment_score * 0.60) + (project_score * 0.40)))
        confidence_score = 90 if assessment_score >= 70 else 65
        confidence = "HIGH" if confidence_score >= 75 else "MEDIUM"
        status = "VERIFIED" if assessment_score >= 70 else "PARTIALLY VERIFIED"
        notes.append(f"Assessment Evidence: {assessment_score} (60% weight)")
        notes.append(f"Project Evidence: {project_score} (40% weight)")
        notes.append(
            "Practical assessment and project evidence both meet verification requirements"
            if status == "VERIFIED"
            else "Practical assessment is below the 70% verification threshold"
        )
    elif assessment_score is not None:
        verified_score = assessment_score
        confidence_score = 65
        confidence = "MEDIUM"
        status = "PARTIALLY VERIFIED"
        notes.append(f"Assessment Evidence: {assessment_score} (100% available weight)")
        notes.append("Limited Evidence: Add project evidence to upgrade confidence to HIGH")
    elif project_score is not None:
        verified_score = int(round(project_score * 0.85))
        confidence_score = 50
        confidence = "MEDIUM"
        status = "PARTIALLY VERIFIED"
        notes.append(f"Project Evidence: {project_score} (Discounted 15% without formal assessment)")
        notes.append("Limited Evidence: Complete skill assessment to achieve full verification")
    else:
        # No empirical evidence at all: self-claim discounted by 50%
        verified_score = int(round(claimed_score * 0.50))
        confidence_score = 25
        confidence = "LOW"
        status = "INSUFFICIENT EVIDENCE"
        notes.append(f"Self-declared: {claimed_score} ({claimed_level})")
        notes.append("No objective evidence found. Self-claim discounted by 50%.")

    return {
        "skill": skill,
        "claimed_score": claimed_score,
        "claimed_level": claimed_level,
        "assessment_score": assessment_score,
        "project_score": project_score,
        "verified_score": verified_score,
        "confidence": confidence,
        "confidence_score": confidence_score,
        "status": status,
        "evidence_notes": notes
    }

async def get_or_create_user_evidence(user_id: str) -> Dict[str, Any]:
    db = get_database()
    now_str = datetime.now(timezone.utc).isoformat()

    # 1. Retrieve student profile
    profile = None
    if db is not None:
        profile = await db.student_profiles.find_one({"user_id": user_id})
    if not profile:
        profile = {"technical_skills": {}, "soft_skills": []}

    claimed_skills = profile.get("technical_skills", {})
    for skill in profile.get("soft_skills", []):
        claimed_skills.setdefault(skill, 50)

    # Only practical, skill-specific assessments provide assessment evidence.
    skill_assessment_scores: Dict[str, int] = profile.get("practical_skill_results", {})

    # 3. Retrieve user's submitted projects
    projects = []
    certificates = []
    if db is not None:
        cursor = db.project_evidence.find({"user_id": user_id}).sort("created_at", -1)
        projects = await cursor.to_list(length=50)
        certificate_cursor = db.certificate_evidence.find({"user_id": user_id}).sort("created_at", -1)
        certificates = await certificate_cursor.to_list(length=50)

    # Compute best project score for each skill
    skill_project_scores: Dict[str, int] = {}
    for p in projects:
        p_score = p.get("verified_score") or calculate_project_score(p)
        for s in p.get("skills_used", []):
            if s not in skill_project_scores or p_score > skill_project_scores[s]:
                skill_project_scores[s] = p_score

    # 4. Generate evidence item for each claimed skill (and any skills in projects/assessments)
    all_skills = set(claimed_skills.keys()) | set(skill_assessment_scores.keys()) | set(skill_project_scores.keys())
    
    evidence_items = []
    total_confidence = 0
    verified_count = 0
    partial_count = 0

    for skill in sorted(all_skills):
        claimed_sc = claimed_skills.get(skill, 50)
        ass_sc = skill_assessment_scores.get(skill)
        proj_sc = skill_project_scores.get(skill)

        item = compute_evidence_for_skill(skill, claimed_sc, ass_sc, proj_sc)
        evidence_items.append(item)

        total_confidence += item["confidence_score"]
        if item["status"] == "VERIFIED":
            verified_count += 1
        elif item["status"] == "PARTIALLY VERIFIED":
            partial_count += 1

        # Persist to MongoDB skill_evidence
        if db is not None:
            await db.skill_evidence.update_one(
                {"user_id": user_id, "skill": skill},
                {"$set": {
                    **item,
                    "user_id": user_id,
                    "updated_at": now_str
                }},
                upsert=True
            )

    avg_conf = int(total_confidence / len(evidence_items)) if evidence_items else 0
    overall_status = "VERIFIED" if avg_conf >= 75 else ("PARTIALLY VERIFIED" if avg_conf >= 50 else "INSUFFICIENT EVIDENCE")

    # Format projects for response
    formatted_projects = []
    for p in projects:
        formatted_projects.append({
            "id": str(p.get("_id", p.get("id"))),
            "user_id": user_id,
            "title": p.get("title", ""),
            "description": p.get("description", ""),
            "skills_used": p.get("skills_used", []),
            "project_type": p.get("project_type", "Academic"),
            "completion_status": p.get("completion_status", "Completed"),
            "project_link": p.get("project_link", ""),
            "github_link": p.get("github_link", ""),
            "student_role": p.get("student_role", "Developer"),
            "verified_score": p.get("verified_score", 80),
            "created_at": p.get("created_at", now_str)
        })

    formatted_certificates = []
    for certificate in certificates:
        formatted_certificates.append({
            "id": str(certificate.get("_id", certificate.get("id"))),
            "user_id": user_id,
            "title": certificate.get("title", ""),
            "issuer": certificate.get("issuer", ""),
            "skills": certificate.get("skills", []),
            "issue_date": certificate.get("issue_date", ""),
            "credential_url": certificate.get("credential_url", ""),
            "created_at": certificate.get("created_at", now_str),
        })

    return {
        "user_id": user_id,
        "skills": evidence_items,
        "total_claimed": len(evidence_items),
        "total_verified": verified_count,
        "total_partially_verified": partial_count,
        "average_confidence": avg_conf,
        "overall_evidence_status": overall_status,
        "projects": formatted_projects,
        "certificates": formatted_certificates,
    }

async def add_project_evidence(user_id: str, project_data: Dict[str, Any]) -> Dict[str, Any]:
    db = get_database()
    now_str = datetime.now(timezone.utc).isoformat()

    verified_score = calculate_project_score(project_data)

    doc = {
        "user_id": user_id,
        "title": project_data.get("title"),
        "description": project_data.get("description"),
        "skills_used": project_data.get("skills_used", []),
        "project_type": project_data.get("project_type", "Academic"),
        "completion_status": project_data.get("completion_status", "Completed"),
        "project_link": project_data.get("project_link", ""),
        "github_link": project_data.get("github_link", ""),
        "student_role": project_data.get("student_role", "Developer"),
        "verified_score": verified_score,
        "created_at": now_str
    }

    if db is not None:
        res = await db.project_evidence.insert_one(doc)
        doc["id"] = str(res.inserted_id)
    else:
        doc["id"] = "mock_proj_" + str(int(datetime.now().timestamp()))

    # Trigger evidence recalculation
    await get_or_create_user_evidence(user_id)

    return doc

async def add_certificate_evidence(user_id: str, certificate_data: Dict[str, Any]) -> Dict[str, Any]:
    db = get_database()
    if db is None:
        raise RuntimeError("Certificate evidence requires an active MongoDB connection.")
    now_str = datetime.now(timezone.utc).isoformat()
    doc = {
        "user_id": user_id,
        "title": certificate_data["title"],
        "issuer": certificate_data["issuer"],
        "skills": certificate_data["skills"],
        "issue_date": certificate_data.get("issue_date", ""),
        "credential_url": certificate_data.get("credential_url", ""),
        "created_at": now_str,
    }
    result = await db.certificate_evidence.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    await get_or_create_user_evidence(user_id)
    return doc

async def get_verified_skills_dict(user_id: str) -> Dict[str, int]:
    db = get_database()
    verified_map = {}
    if db is not None:
        cursor = db.skill_evidence.find({"user_id": user_id})
        items = await cursor.to_list(length=100)
        if items:
            for it in items:
                verified_map[it["skill"]] = it["verified_score"]
            return verified_map

    # Fallback to computing on the fly
    evidence_res = await get_or_create_user_evidence(user_id)
    for it in evidence_res["skills"]:
        verified_map[it["skill"]] = it["verified_score"]
    return verified_map
