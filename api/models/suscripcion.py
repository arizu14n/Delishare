from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
