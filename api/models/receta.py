# -*- coding: utf-8 -*-
"""
Define los modelos de datos para las recetas.

Este archivo contiene:
- `RecetaBase`: Un modelo Pydantic que define los campos base para una receta.
- `RecetaCreate`: Un modelo Pydantic para la creación de una nueva receta, con validaciones.
- `Receta`: Un modelo Pydantic que representa una receta completa, incluyendo campos adicionales.
- `RecetaDB`: Un modelo SQLAlchemy que define la tabla `recetas` en la base de datos.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import NVARCHAR
from ..database import Base

# -------------------
# Modelos Pydantic
# -------------------

class RecetaBase(BaseModel):
    """
    Modelo Pydantic base para una receta.

    Define los campos comunes que se utilizan para la creación y representación de una receta.
    """
    titulo: str
    descripcion: Optional[str] = None
    ingredientes: str
    instrucciones: str
    dificultad: Optional[str] = 'Fácil'
    categoria_id: int
    imagen_url: Optional[str] = None
    autor: Optional[str] = 'Anónimo'
    es_premium: Optional[bool] = False
    activo: Optional[bool] = True
    updated_at: Optional[datetime] = None

class RecetaCreate(RecetaBase):
    """
    Modelo Pydantic para la creación de una nueva receta.

    Hereda de `RecetaBase` y añade validaciones para `tiempo_preparacion` y `porciones`.
    Se utiliza para validar los datos de entrada al crear una nueva receta.
    `Field` se usa para añadir validaciones a los campos.
    """
    tiempo_preparacion: int = Field(..., gt=0, description="Tiempo de preparación en minutos, debe ser mayor a 0.")
    porciones: int = Field(..., gt=0, le=20, description="Número de porciones, debe ser mayor a 0 y menor o igual a 20.")

class Receta(RecetaBase):
    """
    Modelo Pydantic para representar una receta completa.

    Hereda de `RecetaBase` y añade campos que son generados por la base de datos
    o que se obtienen de otras tablas (como `categoria_nombre`).
    """
    id: int
    categoria_nombre: Optional[str] = None  # Este campo se poblará con un JOIN
    vistas: int
    likes: int
    created_at: datetime

    class Config:
        """
        Configuración del modelo Pydantic.

        `from_attributes = True` permite que el modelo Pydantic se cree a partir de
        un objeto SQLAlchemy.
        """
        from_attributes = True

# -------------------
# Modelo SQLAlchemy
# -------------------

class RecetaDB(Base):
    """
    Modelo SQLAlchemy para la tabla `recetas`.

    Define la estructura de la tabla `recetas` en la base de datos.
    """
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(NVARCHAR('max'), nullable=True)
    ingredientes = Column(NVARCHAR('max'), nullable=False)
    instrucciones = Column(NVARCHAR('max'), nullable=False)
    tiempo_preparacion = Column(Integer, default=0)
    porciones = Column(Integer, default=1)
    dificultad = Column(String(50), default='Fácil')
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    imagen_url = Column(String(500), nullable=True)
    autor = Column(String(100), default='Anónimo')
    es_premium = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    vistas = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Define la relación con la tabla `categorias`.
    # Esto permite acceder a la categoría de una receta como un objeto.
    categoria = relationship("CategoriaDB")