from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.incident import Incident, IncidentStatus
from app.models.user import User
from app.schemas.incident import IncidentCreate, IncidentRead, IncidentUpdateStatus
from app.core.dependencies import get_current_user
from app.core.permissions import require_role
from datetime import datetime
from typing import Optional
from datetime import date
from sqlalchemy import and_

router = APIRouter(prefix="/incidents", tags=["Incidents"])

# Criar incidente (operador ou admin)
@router.post("/", response_model=IncidentRead)
async def create_incident(
    data: IncidentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("operador", "admin"))
):
    incident = Incident(
        title=data.title,
        description=data.description,
        reporter_id=user.id
    )
    db.add(incident)
    await db.commit()
    await db.refresh(incident)
    return incident

# Lista os incidentes podendo filtrar
@router.get("/", response_model=list[IncidentRead])
async def list_incidents(
    status: Optional[IncidentStatus] = None,
    reporter_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    query = select(Incident)

    filters = []

    if status:
        filters.append(Incident.status == status)
    if reporter_id:
        filters.append(Incident.reporter_id == reporter_id)
    if from_date:
        filters.append(Incident.created_at >= from_date)
    if to_date:
        filters.append(Incident.created_at <= to_date)

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query)
    return result.scalars().all()

# Atualizar status do incidente (admin)
@router.patch("/{incident_id}/status", response_model=IncidentRead)
async def update_status(
    incident_id: int,
    data: IncidentUpdateStatus,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    result = await db.execute(select(Incident).where(Incident.id == incident_id))
    incident = result.scalar_one_or_none()
    if not incident:
        raise HTTPException(status_code=404, detail="Incidente não encontrado")

    incident.status = data.status
    if data.status == IncidentStatus.RESOLVIDO:
        incident.resolved_at = datetime.utcnow()
        incident.resolver_id = user.id

    await db.commit()
    await db.refresh(incident)
    return incident
