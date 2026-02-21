"""
Modelo de Cliente
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.config.database import Base


class Cliente(Base):
    """
    Modelo de Cliente - Dueños de las mascotas
    """
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    direccion = Column(String(200), nullable=True)
    documento = Column(String(20), unique=True, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    notas = Column(String(500), nullable=True)
    
    # Relaciones
    mascotas = relationship("Mascota", back_populates="cliente", cascade="all, delete-orphan")
    ventas = relationship("Venta", back_populates="cliente")
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del cliente"""
        return f"{self.nombre} {self.apellido}"
    
    def __repr__(self):
        return f"<Cliente {self.nombre_completo}>"
