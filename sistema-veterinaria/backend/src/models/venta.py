"""
Modelos de Venta y DetalleVenta
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.config.database import Base


class Venta(Base):
    """
    Modelo de Venta - Registro de ventas realizadas
    """
    __tablename__ = "ventas"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_venta = Column(String(50), unique=True, index=True, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    subtotal = Column(Float, nullable=False)
    descuento = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    metodo_pago = Column(String(50), nullable=False)  # Efectivo, Tarjeta, Transferencia
    estado = Column(String(20), default="completada")  # completada, cancelada, pendiente
    notas = Column(String(500), nullable=True)
    
    # Claves foráneas
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="ventas")
    usuario = relationship("Usuario", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Venta {self.codigo_venta} - Total: ${self.total}>"


class DetalleVenta(Base):
    """
    Modelo de DetalleVenta - Productos incluidos en cada venta
    """
    __tablename__ = "detalles_venta"
    
    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    # Claves foráneas
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    
    # Relaciones
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_venta")
    
    def __repr__(self):
        return f"<DetalleVenta venta_id={self.venta_id} producto_id={self.producto_id}>"
