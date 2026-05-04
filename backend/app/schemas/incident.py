from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.incident import IncidentSeverity, IncidentStatus, IncidentType


class IncidentCreate(BaseModel):
    title: str = Field(min_length=5, max_length=160)
    description: str = Field(min_length=10)
    incident_type: IncidentType
    severity: IncidentSeverity
    reported_by: str = Field(min_length=3, max_length=120)
    student_name: str = Field(min_length=3, max_length=120)
    course: str = Field(min_length=2, max_length=40)
    occurred_at: datetime


class IncidentRead(BaseModel):
    id: UUID
    title: str
    description: str
    incident_type: IncidentType
    severity: IncidentSeverity
    status: IncidentStatus
    reported_by: str
    student_name: str
    course: str
    occurred_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
