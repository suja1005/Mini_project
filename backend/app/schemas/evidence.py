from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ProjectEvidenceCreate(BaseModel):
    title: str = Field(..., min_length=2)
    description: str = Field(..., min_length=5)
    skills_used: List[str] = Field(..., min_length=1)
    project_type: str = "Academic"  # Academic, Capstone, Personal, Hackathon, Open Source
    completion_status: str = "Completed"  # Completed, In Progress
    project_link: Optional[str] = ""
    github_link: Optional[str] = ""
    student_role: Optional[str] = "Developer"

class ProjectEvidenceResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    skills_used: List[str]
    project_type: str
    completion_status: str
    project_link: Optional[str] = ""
    github_link: Optional[str] = ""
    student_role: Optional[str] = "Developer"
    verified_score: int
    created_at: str

class SkillEvidenceItem(BaseModel):
    skill: str
    claimed_score: int
    claimed_level: str  # Beginner (30), Intermediate (60), Advanced (85)
    assessment_score: Optional[int] = None
    project_score: Optional[int] = None
    verified_score: int
    confidence: str  # LOW, MEDIUM, HIGH
    confidence_score: int  # 0-100
    status: str  # VERIFIED, PARTIALLY VERIFIED, INSUFFICIENT EVIDENCE
    evidence_notes: List[str] = []

class EvidenceOverviewResponse(BaseModel):
    user_id: str
    skills: List[SkillEvidenceItem]
    total_claimed: int
    total_verified: int
    total_partially_verified: int
    average_confidence: int
    overall_evidence_status: str
    projects: List[ProjectEvidenceResponse] = []

class VerifiedSkillsResponse(BaseModel):
    user_id: str
    verified_skills: Dict[str, int]
    confidence_levels: Dict[str, str]
