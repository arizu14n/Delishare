from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, func
from ..database import Base

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z\s]+$")
    email: EmailStr
    tipo_suscripcion: Optional[str] = 'gratuito'
    fecha_suscripcion: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    activo: Optional[bool] = True
    intentos_login: Optional[int] = 0
    bloqueado_hasta: Optional[datetime] = None
    ultimo_login: Optional[datetime] = None

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8, max_length=20, pattern="^[a-zA-Z0-9!@#$%^&*]{8,20}$", title="La contraseña debe tener entre 8 y 20 caracteres, y puede contener letras, números y los símbolos !@#$%^&*")

class UsuarioInDB(UsuarioBase):
    id: int
    password_hash: str # Hash de la contraseña almacenado en DB
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Usuario(UsuarioBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UsuarioDB(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    tipo_suscripcion = Column(String(50), default='gratuito')
    fecha_suscripcion = Column(Date, nullable=True)
    fecha_vencimiento = Column(Date, nullable=True)
    activo = Column(Boolean, default=True)
    intentos_login = Column(Integer, default=0)
    bloqueado_hasta = Column(DateTime, nullable=True)
    ultimo_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
