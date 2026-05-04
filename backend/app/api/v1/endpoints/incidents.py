from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud.incident import create_incident, get_incident, list_incidents
from app.models.incident import IncidentStatus, IncidentType
from app.schemas.incident import IncidentCreate, IncidentRead

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
async def create_incident_endpoint(payload: IncidentCreate, db: AsyncSession = Depends(get_db)) -> IncidentRead:
    incident = await create_incident(db, payload)
    return IncidentRead.model_validate(incident)


@router.get("", response_model=list[IncidentRead])
async def list_incidents_endpoint(
    incident_type: IncidentType | None = Query(default=None),
    status: IncidentStatus | None = Query(default=None),
    course: str | None = Query(default=None),
    student_name: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[IncidentRead]:
    incidents = await list_incidents(
        db=db,
        incident_type=incident_type,
        status=status,
        course=course,
        student_name=student_name,
        search=search,
    )
    return [IncidentRead.model_validate(item) for item in incidents]


@router.get("/{incident_id}", response_model=IncidentRead)
async def get_incident_endpoint(incident_id: UUID, db: AsyncSession = Depends(get_db)) -> IncidentRead:
    incident = await get_incident(db, incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return IncidentRead.model_validate(incident)
