from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, func
from ..database import Base

class PlanSuscripcionBase(BaseModel):
    nombre: str
    precio: float
    duracion_dias: int
    descripcion: Optional[str] = None
    activo: Optional[bool] = True

class PlanSuscripcion(PlanSuscripcionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SuscripcionUpdate(BaseModel):
    usuario_id: int
    plan: str

class PlanSuscripcionDB(Base):
    __tablename__ = "planes_suscripcion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    precio = Column(Float, nullable=False)
    duracion_dias = Column(Integer, nullable=False)
    descripcion = Column(String(500), nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
