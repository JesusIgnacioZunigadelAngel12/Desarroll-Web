"""
Schemas de autenticación y usuario
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UsuarioBase(BaseModel):
    """Schema base de Usuario"""
    username: str
    email: EmailStr
    nombre_completo: str
    rol: str = "usuario"


class UsuarioCreate(UsuarioBase):
    """Schema para crear un usuario"""
    password: str


class UsuarioUpdate(BaseModel):
    """Schema para actualizar un usuario"""
    email: Optional[EmailStr] = None
    nombre_completo: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    """Schema de respuesta de Usuario"""
    id: int
    activo: bool
    fecha_creacion: datetime
    ultimo_acceso: Optional[datetime]
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema para el token JWT"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Datos contenidos en el token"""
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema para request de login"""
    username: str
    password: str
