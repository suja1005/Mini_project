from pydantic import BaseModel
from typing import List, Optional

class EmployabilityHistoryPoint(BaseModel):
    date: str
    score: int
    milestone: str
    timestamp: str

class SkillProgressItem(BaseModel):
    skill: str
    initial_score: int
    current_score: int
    target_score: int
    gap: int
    improvement: int
    status: str  # ON_TRACK, NEEDS_ATTENTION, ACHIEVED

class ProgressOverviewResponse(BaseModel):
    user_id: str
    target_career: str
    current_employability: int
    previous_employability: int
    target_employability: int
    employability_gap: int
    improvement_delta: int
    completed_tasks_count: int
    total_tasks_count: int
    task_completion_rate: int
    verified_skills_count: int
    partial_skills_count: int
    history: List[EmployabilityHistoryPoint]
    skill_progress: List[SkillProgressItem]

class EmployabilityProgressResponse(BaseModel):
    current_employability: int
    previous_employability: int
    target_employability: int
    employability_gap: int
    improvement_delta: int
    status: str
