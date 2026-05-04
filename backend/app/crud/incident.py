from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.incident import Incident, IncidentStatus, IncidentType
from app.schemas.incident import IncidentCreate


async def create_incident(db: AsyncSession, payload: IncidentCreate) -> Incident:
    incident = Incident(**payload.model_dump())
    db.add(incident)
    await db.commit()
    await db.refresh(incident)
    return incident


async def list_incidents(
    db: AsyncSession,
    incident_type: IncidentType | None = None,
    status: IncidentStatus | None = None,
    course: str | None = None,
    student_name: str | None = None,
    search: str | None = None,
) -> list[Incident]:
    query = select(Incident)

    if incident_type:
        query = query.where(Incident.incident_type == incident_type)
    if status:
        query = query.where(Incident.status == status)
    if course:
        query = query.where(Incident.course.ilike(f"%{course}%"))
    if student_name:
        query = query.where(Incident.student_name.ilike(f"%{student_name}%"))
    if search:
        query = query.where(
            or_(
                Incident.title.ilike(f"%{search}%"),
                Incident.description.ilike(f"%{search}%"),
            )
        )

    query = query.order_by(Incident.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_incident(db: AsyncSession, incident_id: UUID) -> Incident | None:
    result = await db.execute(select(Incident).where(Incident.id == incident_id))
    return result.scalar_one_or_none()
