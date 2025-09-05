# -*- coding: utf-8 -*-
"""
Define los modelos de datos para las categorías de recetas.

Este archivo contiene:
- `CategoriaBase`: Un modelo Pydantic que define los campos base para una categoría.
- `CategoriaCreate`: Un modelo Pydantic para la creación de una nueva categoría.
- `Categoria`: Un modelo Pydantic que representa una categoría con su ID y fecha de creación.
- `CategoriaDB`: Un modelo SQLAlchemy que define la tabla `categorias` en la base de datos.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from ..database import Base

# -------------------
# Modelos Pydantic
# -------------------

class CategoriaBase(BaseModel):
    """
    Modelo Pydantic base para una categoría.

    Define los campos comunes que se utilizan tanto para la creación como para la
    representación de una categoría.
    """
    nombre: str
    descripcion: Optional[str] = None
    icono: Optional[str] = 'fas fa-utensils'  # Icono de Font Awesome por defecto
    activo: Optional[bool] = True
    orden: Optional[int] = 0

class CategoriaCreate(CategoriaBase):
    """
    Modelo Pydantic para la creación de una nueva categoría.

    Hereda de `CategoriaBase` y no añade campos adicionales. Se utiliza para
    validar los datos de entrada al crear una nueva categoría.
    """
    pass

class Categoria(CategoriaBase):
    """
    Modelo Pydantic para representar una categoría.

    Hereda de `CategoriaBase` y añade los campos `id` y `created_at`, que son
    generados por la base de datos.
    """
    id: int
    created_at: datetime

    class Config:
        """
        Configuración del modelo Pydantic.

        `from_attributes = True` permite que el modelo Pydantic se cree a partir de
        un objeto SQLAlchemy (o cualquier otro objeto con atributos).
        """
        from_attributes = True

# -------------------
# Modelo SQLAlchemy
# -------------------

class CategoriaDB(Base):
    """
    Modelo SQLAlchemy para la tabla `categorias`.

    Define la estructura de la tabla `categorias` en la base de datos, incluyendo
    el nombre de la tabla, las columnas y sus tipos de datos.
    """
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(500), nullable=True)
    icono = Column(String(50), default='fas fa-utensils')
    activo = Column(Boolean, default=True)
    orden = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())