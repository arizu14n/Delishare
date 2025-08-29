from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
