from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import sqlalchemy as sa


class IncidentStatus(PyEnum):
    ABERTO = "aberto"
    EM_ANDAMENTO = "em_andamento"
    RESOLVIDO = "resolvido"

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(sa.Enum(IncidentStatus, name="incident_status"), default=IncidentStatus.ABERTO, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resolver_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    reporter = relationship("User", foreign_keys=[reporter_id], backref="reported_incidents")
    resolver = relationship("User", foreign_keys=[resolver_id], backref="resolved_incidents")