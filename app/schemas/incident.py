from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.incident import IncidentStatus

class IncidentCreate(BaseModel):
    title: str
    description: str

class IncidentRead(BaseModel):
    id: int
    title: str
    description: str
    status: IncidentStatus
    created_at: datetime
    resolved_at: Optional[datetime]
    reporter_id: int
    resolver_id: Optional[int]

    class Config:
        orm_mode = True

class IncidentUpdateStatus(BaseModel):
    status: IncidentStatus