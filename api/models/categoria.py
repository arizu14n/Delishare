from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from ..database import Base

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    icono: Optional[str] = 'fas fa-utensils'
    activo: Optional[bool] = True
    orden: Optional[int] = 0

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CategoriaDB(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(500), nullable=True)
    icono = Column(String(50), default='fas fa-utensils')
    activo = Column(Boolean, default=True)
    orden = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
