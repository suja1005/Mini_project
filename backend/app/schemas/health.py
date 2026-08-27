from pydantic import BaseModel
from typing import Dict, Any

class HealthResponse(BaseModel):
    status: str
    version: str
    service: str
    database_connected: bool
    phase: str
    active_modules: Dict[str, bool]
