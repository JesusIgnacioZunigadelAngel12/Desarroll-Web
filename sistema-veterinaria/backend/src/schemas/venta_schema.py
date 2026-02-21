"""
Schemas para Venta y DetalleVenta
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class DetalleVentaBase(BaseModel):
    """Schema base de DetalleVenta"""
    producto_id: int
    cantidad: int
    precio_unitario: float


class DetalleVentaCreate(DetalleVentaBase):
    """Schema para crear un detalle de venta"""
    pass


class DetalleVentaResponse(DetalleVentaBase):
    """Schema de respuesta de DetalleVenta"""
    id: int
    subtotal: float
    
    class Config:
        from_attributes = True


class VentaBase(BaseModel):
    """Schema base de Venta"""
    metodo_pago: str
    descuento: float = 0.0
    notas: Optional[str] = None


class VentaCreate(VentaBase):
    """Schema para crear una venta"""
    cliente_id: Optional[int] = None
    detalles: List[DetalleVentaCreate]


class VentaResponse(VentaBase):
    """Schema de respuesta de Venta"""
    id: int
    codigo_venta: str
    fecha: datetime
    subtotal: float
    total: float
    estado: str
    cliente_id: Optional[int]
    usuario_id: int
    detalles: List[DetalleVentaResponse] = []
    
    class Config:
        from_attributes = True


class VentaStats(BaseModel):
    """Estadísticas de ventas"""
    total_ventas: int
    monto_total: float
    promedio_venta: float
    ventas_hoy: int
    monto_hoy: float
