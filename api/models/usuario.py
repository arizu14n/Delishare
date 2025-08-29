from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date

class UsuarioBase(BaseModel):
    nombre: str
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
    password: str # Hash de la contraseña almacenado en DB
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Usuario(UsuarioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
