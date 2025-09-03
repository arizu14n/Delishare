from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import NVARCHAR
from ..database import Base

# Modelo base con los campos comunes de una receta
class RecetaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    ingredientes: str
    instrucciones: str
    tiempo_preparacion: Optional[int] = 0
    porciones: Optional[int] = 1
    dificultad: Optional[str] = 'Fácil'
    categoria_id: int
    imagen_url: Optional[str] = None
    autor: Optional[str] = 'Anónimo'
    es_premium: Optional[bool] = False
    activo: Optional[bool] = True
    updated_at: Optional[datetime] = None

# Modelo para la creación de una receta (lo que se espera en un POST)
class RecetaCreate(RecetaBase):
    pass

# Modelo para la respuesta de la API (lo que se devuelve en un GET)
class Receta(RecetaBase):
    id: int
    categoria_nombre: Optional[str] = None # Se obtendrá con un JOIN
    vistas: int
    likes: int
    created_at: datetime

    class Config:
        from_attributes = True # Permite mapear directamente desde objetos de base de datos

class RecetaDB(Base):
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

    categoria = relationship("CategoriaDB")
