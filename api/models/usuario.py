# -*- coding: utf-8 -*-
"""
Define los modelos de datos para los usuarios.

Este archivo contiene:
- `UsuarioBase`: Un modelo Pydantic que define los campos base para un usuario.
- `UsuarioCreate`: Un modelo Pydantic para la creación de un nuevo usuario, con validación de contraseña.
- `UsuarioInDB`: Un modelo Pydantic que representa un usuario tal como se almacena en la base de datos (con el hash de la contraseña).
- `Usuario`: Un modelo Pydantic que representa un usuario para ser devuelto por la API (sin la contraseña).
- `UsuarioDB`: Un modelo SQLAlchemy que define la tabla `usuario` en la base de datos.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, func
from ..database import Base

# -------------------
# Modelos Pydantic
# -------------------

class UsuarioBase(BaseModel):
    """
    Modelo Pydantic base para un usuario.

    Define los campos comunes que se utilizan para la creación y representación de un usuario.
    """
    nombre: str
    email: EmailStr  # Valida que el campo sea un email válido.
    tipo_suscripcion: Optional[str] = 'gratuito'
    fecha_suscripcion: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    activo: Optional[bool] = True
    intentos_login: Optional[int] = 0
    bloqueado_hasta: Optional[datetime] = None
    ultimo_login: Optional[datetime] = None

class UsuarioCreate(UsuarioBase):
    """
    Modelo Pydantic para la creación de un nuevo usuario.

    Hereda de `UsuarioBase` y añade el campo `password` con validaciones específicas.
    Se utiliza para validar los datos de entrada al registrar un nuevo usuario.
    """
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
        pattern="^[a-zA-Z0-9!@#$%^&*]{8,20}$",
        title="La contraseña debe tener entre 8 y 20 caracteres, y puede contener letras, números y los símbolos !@#$%^&*"
    )

class UsuarioInDB(UsuarioBase):
    """
    Modelo Pydantic que representa un usuario en la base de datos.

    Hereda de `UsuarioBase` y añade el `id` y el `password_hash`.
    Este modelo se utiliza internamente para manejar los datos del usuario
    incluyendo el hash de la contraseña.
    """
    id: int
    password_hash: str  # Hash de la contraseña almacenado en la base de datos.
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Usuario(UsuarioBase):
    """
    Modelo Pydantic para representar un usuario en las respuestas de la API.

    Hereda de `UsuarioBase` y añade el `id` y las fechas de creación/actualización.
    **Importante:** Este modelo no incluye la contraseña ni su hash, por lo que es
    seguro para ser devuelto en las respuestas de la API.
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# -------------------
# Modelo SQLAlchemy
# -------------------

class UsuarioDB(Base):
    """
    Modelo SQLAlchemy para la tabla `usuario`.

    Define la estructura de la tabla `usuario` en la base de datos.
    """
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # Se almacena el hash, no la contraseña en texto plano.
    tipo_suscripcion = Column(String(50), default='gratuito')
    fecha_suscripcion = Column(Date, nullable=True)
    fecha_vencimiento = Column(Date, nullable=True)
    activo = Column(Boolean, default=True)
    intentos_login = Column(Integer, default=0)
    bloqueado_hasta = Column(DateTime, nullable=True)
    ultimo_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())