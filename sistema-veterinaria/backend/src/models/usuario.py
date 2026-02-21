"""
Modelo de Usuario para el sistema de autenticación
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.config.database import Base


class Usuario(Base):
    """
    Modelo de Usuario para autenticación y gestión de accesos
    """
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    rol = Column(String(20), default="usuario")  # admin, veterinario, usuario
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    ultimo_acceso = Column(DateTime, nullable=True)
    
    # Relaciones
    ventas = relationship("Venta", back_populates="usuario")
    
    def __repr__(self):
        return f"<Usuario {self.username}>"
