from pydantic import BaseModel
from typing import List, Dict, Optional

class SkillProficiency(BaseModel):
    name: str
    level: str  # Beginner, Intermediate, Advanced
    score: int  # 30, 60, 85

class StudentProfileSchema(BaseModel):
    full_name: str
    degree: str
    department: str
    year_of_study: str
    cgpa: str
    technical_skills: Dict[str, int] = {}  # e.g., {"Python": 85, "ML": 60}
    soft_skills: List[str] = []
    interests: List[str] = []
    aptitude_scores: Dict[str, int] = {
        "logical_reasoning": 70,
        "numerical_ability": 70,
        "analytical_thinking": 70
    }
    target_role: Optional[str] = "AI Engineer"
    preferred_domain: Optional[str] = "Artificial Intelligence"

class StudentProfileResponse(StudentProfileSchema):
    user_id: str
    is_complete: bool = True
