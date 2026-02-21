"""
Modelo de Producto
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.config.database import Base


class Producto(Base):
    """
    Modelo de Producto - Para inventario y ventas
    """
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, index=True, nullable=False)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(500), nullable=True)
    categoria = Column(String(50), nullable=False)  # Medicamento, Alimento, Accesorio, Servicio
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=5)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    detalles_venta = relationship("DetalleVenta", back_populates="producto")
    
    @property
    def requiere_reposicion(self):
        """Verifica si el producto necesita reposición"""
        return self.stock <= self.stock_minimo
    
    def __repr__(self):
        return f"<Producto {self.codigo} - {self.nombre}>"
