"""
Schemas para Mascota
"""
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class MascotaBase(BaseModel):
    """Schema base de Mascota"""
    nombre: str
    especie: str
    raza: Optional[str] = None
    edad: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[str] = None
    color: Optional[str] = None
    peso: Optional[float] = None
    observaciones: Optional[str] = None


class MascotaCreate(MascotaBase):
    """Schema para crear una mascota"""
    cliente_id: int


class MascotaUpdate(BaseModel):
    """Schema para actualizar una mascota"""
    nombre: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    edad: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[str] = None
    color: Optional[str] = None
    peso: Optional[float] = None
    observaciones: Optional[str] = None


class MascotaResponse(MascotaBase):
    """Schema de respuesta de Mascota"""
    id: int
    cliente_id: int
    fecha_registro: datetime
    
    class Config:
        from_attributes = True
