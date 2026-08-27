import json
from pathlib import Path
from typing import List, Dict, Any

def load_careers_data() -> List[Dict[str, Any]]:
    json_path = Path(__file__).resolve().parent.parent.parent / "data" / "careers.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def calculate_technical_match(student_skills: Dict[str, int], required_skills: Dict[str, int]) -> float:
    if not required_skills:
        return 50.0
    total_score = 0.0
    for skill, req_level in required_skills.items():
        curr_level = student_skills.get(skill, 0)
        # Match ratio capped at 100%
        ratio = min(1.0, curr_level / float(req_level)) if req_level > 0 else 1.0
        total_score += ratio * 100.0
    return total_score / len(required_skills)

def calculate_interest_match(student_interests: List[str], career_category: str) -> float:
    if not student_interests:
        return 50.0
    for interest in student_interests:
        if interest.lower() in career_category.lower() or career_category.lower() in interest.lower():
            return 95.0
    return 60.0

def calculate_aptitude_match(student_aptitude: Dict[str, int], required_aptitude: Dict[str, int]) -> float:
    if not required_aptitude:
        return 70.0
    scores = []
    for k, req in required_aptitude.items():
        curr = student_aptitude.get(k, 60)
        scores.append(min(100.0, (curr / float(req)) * 100.0 if req > 0 else 100.0))
    return sum(scores) / len(scores) if scores else 70.0

def calculate_academic_match(student_degree: str, academic_relevance: List[str]) -> float:
    if not academic_relevance:
        return 80.0
    for deg in academic_relevance:
        if deg.lower() in student_degree.lower() or student_degree.lower() in deg.lower():
            return 90.0
    return 70.0

def calculate_preference_match(student_target: str, career_title: str) -> float:
    if not student_target:
        return 70.0
    if student_target.lower() in career_title.lower() or career_title.lower() in student_target.lower():
        return 100.0
    return 65.0

def calculate_career_fit(profile: Dict[str, Any], career: Dict[str, Any]) -> Dict[str, Any]:
    student_skills = profile.get("technical_skills", {})
    student_interests = profile.get("interests", [])
    student_aptitude = profile.get("aptitude_scores", {})
    student_degree = profile.get("degree", "B.Tech")
    student_target = profile.get("target_role", "")

    tech_score = calculate_technical_match(student_skills, career.get("required_skills", {}))
    interest_score = calculate_interest_match(student_interests, career.get("category", ""))
    aptitude_score = calculate_aptitude_match(student_aptitude, career.get("required_aptitude", {}))
    academic_score = calculate_academic_match(student_degree, career.get("academic_relevance", []))
    preference_score = calculate_preference_match(student_target, career.get("title", ""))

    # Explainable Weighted Formula: 40% Tech, 20% Interest, 15% Aptitude, 10% Academic, 15% Preference
    fit_score = int(
        (tech_score * 0.40) +
        (interest_score * 0.20) +
        (aptitude_score * 0.15) +
        (academic_score * 0.10) +
        (preference_score * 0.15)
    )
    fit_score = max(30, min(98, fit_score))

    # Identify strengths and missing areas
    why_recommended = []
    needs_improvement = []

    for skill, req in career.get("required_skills", {}).items():
        curr = student_skills.get(skill, 0)
        if curr >= req - 10:
            why_recommended.append(f"Strong foundation in {skill} ({curr} pts)")
        else:
            needs_improvement.append(f"Requires advancement in {skill} (Current: {curr}, Target: {req})")

    if interest_score >= 80:
        why_recommended.append(f"High interest match with {career.get('category')}")
    if aptitude_score >= 75:
        why_recommended.append("Strong analytical and logical reasoning aptitude")

    if not why_recommended:
        why_recommended.append("Good foundational academic alignment")
    if not needs_improvement:
        needs_improvement.append("Gain practical domain project experience")

    return {
        "id": career.get("id"),
        "title": career.get("title"),
        "category": career.get("category"),
        "description": career.get("description"),
        "fit_score": fit_score,
        "why_recommended": why_recommended[:3],
        "needs_improvement": needs_improvement[:3],
        "learning_difficulty": career.get("learning_difficulty", "MEDIUM")
    }

def generate_user_recommendations(profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    careers = load_careers_data()
    results = []
    for c in careers:
        fit_item = calculate_career_fit(profile, c)
        results.append(fit_item)
    
    # Sort descending by fit_score
    results.sort(key=lambda x: x["fit_score"], reverse=True)
    return results[:4]  # Return top 3-5

def generate_career_analysis(profile: Dict[str, Any], career_id: str) -> Dict[str, Any]:
    careers = load_careers_data()
    career = next((c for c in careers if c["id"] == career_id), None)
    if not career:
        # Fallback to AI Engineer if ID not found
        career = careers[0] if careers else {
            "id": "ai-engineer", "title": "AI Engineer", "category": "Artificial Intelligence",
            "required_skills": {"Python": 85, "Machine Learning": 80, "SQL": 75},
            "required_employability": 80
        }

    fit_info = calculate_career_fit(profile, career)
    fit_score = fit_info["fit_score"]

    student_skills = profile.get("technical_skills", {})
    required_skills = career.get("required_skills", {})

    skill_gaps = []
    total_gap = 0
    high_priority_count = 0

    for skill, req in required_skills.items():
        curr = student_skills.get(skill, 0)
        gap = max(0, req - curr)
        total_gap += gap

        priority = "LOW"
        if gap >= 30:
            priority = "HIGH"
            high_priority_count += 1
        elif gap >= 15:
            priority = "MEDIUM"

        skill_gaps.append({
            "skill": skill,
            "current": curr,
            "required": req,
            "gap": gap,
            "priority": priority
        })

    # Current Employability calculation
    tech_avg = sum(student_skills.values()) / len(student_skills) if student_skills else 40
    apt_avg = sum(profile.get("aptitude_scores", {}).values()) / 3 if profile.get("aptitude_scores") else 70
    current_employability = int((fit_score * 0.50) + (tech_avg * 0.30) + (apt_avg * 0.20))
    current_employability = max(35, min(95, current_employability))

    required_employability = career.get("required_employability", 80)
    employability_gap = max(0, required_employability - current_employability)

    # Learning effort determination
    if total_gap > 70 or high_priority_count >= 2:
        learning_effort = "HIGH"
    elif total_gap > 35:
        learning_effort = "MEDIUM"
    else:
        learning_effort = "LOW"

    # Risk determination
    if fit_score < 65 or employability_gap > 30:
        career_risk = "HIGH"
    elif fit_score < 80 or employability_gap > 15:
        career_risk = "MEDIUM"
    else:
        career_risk = "LOW"

    # Achievability score (0-100)
    achievability = int((fit_score * 0.40) + (current_employability * 0.35) + ((100 - total_gap) * 0.25))
    achievability = max(40, min(96, achievability))

    return {
        "career_id": career["id"],
        "title": career["title"],
        "category": career["category"],
        "fit_score": fit_score,
        "current_employability": current_employability,
        "required_employability": required_employability,
        "employability_gap": employability_gap,
        "learning_effort": learning_effort,
        "career_risk": career_risk,
        "achievability": achievability,
        "skill_gaps": skill_gaps
    }
