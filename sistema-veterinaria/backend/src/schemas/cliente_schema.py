"""
Schemas para Cliente
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from .mascota_schema import MascotaResponse


class ClienteBase(BaseModel):
    """Schema base de Cliente"""
    nombre: str
    apellido: str
    telefono: str
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    documento: Optional[str] = None


class ClienteCreate(ClienteBase):
    """Schema para crear un cliente"""
    pass


class ClienteUpdate(BaseModel):
    """Schema para actualizar un cliente"""
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    documento: Optional[str] = None
    notas: Optional[str] = None


class ClienteResponse(ClienteBase):
    """Schema de respuesta de Cliente"""
    id: int
    fecha_registro: datetime
    notas: Optional[str]
    
    class Config:
        from_attributes = True


class ClienteWithMascotas(ClienteResponse):
    """Cliente con sus mascotas"""
    mascotas: List[MascotaResponse] = []

    model_config = {"from_attributes": True}
