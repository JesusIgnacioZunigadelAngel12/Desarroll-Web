"""
Schemas Pydantic para Citas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CitaBase(BaseModel):
    cliente_id:  int
    mascota_id:  int
    fecha_hora:  datetime
    motivo:      str
    estado:      Optional[str] = "pendiente"
    veterinario: Optional[str] = None
    notas:       Optional[str] = None


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):
    fecha_hora:  Optional[datetime] = None
    motivo:      Optional[str]      = None
    estado:      Optional[str]      = None
    veterinario: Optional[str]      = None
    notas:       Optional[str]      = None


class CitaResponse(CitaBase):
    id:             int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
