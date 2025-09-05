# -*- coding: utf-8 -*-
"""
Define los modelos de datos para los planes de suscripción.

Este archivo contiene:
- `PlanSuscripcionBase`: Un modelo Pydantic que define los campos base para un plan de suscripción.
- `PlanSuscripcion`: Un modelo Pydantic que representa un plan de suscripción completo.
- `SuscripcionUpdate`: Un modelo Pydantic para actualizar la suscripción de un usuario.
- `PlanSuscripcionDB`: Un modelo SQLAlchemy que define la tabla `planes_suscripcion` en la base de datos.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, func
from ..database import Base

# -------------------
# Modelos Pydantic
# -------------------

class PlanSuscripcionBase(BaseModel):
    """
    Modelo Pydantic base para un plan de suscripción.

    Define los campos comunes que se utilizan para la creación y representación de un plan.
    """
    nombre: str
    precio: float
    duracion_dias: int
    descripcion: Optional[str] = None
    activo: Optional[bool] = True

class PlanSuscripcion(PlanSuscripcionBase):
    """
    Modelo Pydantic para representar un plan de suscripción completo.

    Hereda de `PlanSuscripcionBase` y añade campos generados por la base de datos.
    """
    id: int
    created_at: datetime

    class Config:
        """
        Configuración del modelo Pydantic.

        `from_attributes = True` permite que el modelo se cree a partir de un objeto SQLAlchemy.
        """
        from_attributes = True

class SuscripcionUpdate(BaseModel):
    """
    Modelo Pydantic para la actualización de la suscripción de un usuario.

    Se utiliza para validar los datos de entrada al actualizar la suscripción de un usuario.
    """
    usuario_id: int
    plan: str

# -------------------
# Modelo SQLAlchemy
# -------------------

class PlanSuscripcionDB(Base):
    """
    Modelo SQLAlchemy para la tabla `planes_suscripcion`.

    Define la estructura de la tabla `planes_suscripcion` en la base de datos.
    """
    __tablename__ = "planes_suscripcion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    precio = Column(Float, nullable=False)
    duracion_dias = Column(Integer, nullable=False)
    descripcion = Column(String(500), nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())