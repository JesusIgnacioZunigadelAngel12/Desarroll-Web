"""
Schemas para Producto
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductoBase(BaseModel):
    """Schema base de Producto"""
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    categoria: str
    precio: float
    stock: int = 0
    stock_minimo: int = 5


class ProductoCreate(ProductoBase):
    """Schema para crear un producto"""
    pass


class ProductoUpdate(BaseModel):
    """Schema para actualizar un producto"""
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    stock_minimo: Optional[int] = None
    activo: Optional[bool] = None


class ProductoResponse(ProductoBase):
    """Schema de respuesta de Producto"""
    id: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    requiere_reposicion: bool
    
    class Config:
        from_attributes = True
