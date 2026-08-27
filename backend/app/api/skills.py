import json
from pathlib import Path
from fastapi import APIRouter

router = APIRouter(prefix="/skills", tags=["Skills Metadata"])

@router.get("")
async def get_skills():
    json_path = Path(__file__).resolve().parent.parent.parent / "data" / "skills.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "technical_skills": ["Python", "Java", "JavaScript", "HTML", "CSS", "SQL", "Git", "Machine Learning", "Data Analysis", "Cloud", "Cybersecurity", "UI/UX"],
        "proficiency_mapping": {"Beginner": 30, "Intermediate": 60, "Advanced": 85},
        "soft_skills": ["Communication", "Teamwork", "Leadership", "Problem Solving", "Adaptability", "Time Management"],
        "interests": ["Artificial Intelligence", "Data Science", "Software Development", "Cloud Computing", "Cybersecurity", "UI/UX", "Business"]
    }
