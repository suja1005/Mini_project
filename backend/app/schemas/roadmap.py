from pydantic import BaseModel
from typing import List, Optional

class RoadmapTaskSchema(BaseModel):
    id: str
    roadmap_id: str
    phase: int
    phase_name: str
    title: str
    description: str
    skill: str
    type: str  # Learning, Assessment, Project, Practice, Evidence Submission
    priority: str  # HIGH, MEDIUM, LOW
    estimated_effort: str
    status: str = "NOT STARTED"  # NOT STARTED, IN PROGRESS, COMPLETED
    explanation: str
    completed_at: Optional[str] = None

class RoadmapTaskUpdate(BaseModel):
    status: str  # NOT STARTED, IN PROGRESS, COMPLETED

class RoadmapGenerateRequest(BaseModel):
    career_id: Optional[str] = "ai-engineer"

class RoadmapResponse(BaseModel):
    id: str
    user_id: str
    career_id: str
    career_title: str
    target_employability: int
    current_employability: int
    employability_gap: int
    total_tasks: int
    completed_tasks: int
    progress_percentage: int
    phases: List[str]
    tasks: List[RoadmapTaskSchema]
    last_updated: str
