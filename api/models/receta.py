from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
