"""
Modelo de Mascota
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from src.config.database import Base


class Mascota(Base):
    """
    Modelo de Mascota - Pertenece a un Cliente
    """
    __tablename__ = "mascotas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    especie = Column(String(50), nullable=False)  # Perro, Gato, Ave, etc.
    raza = Column(String(100), nullable=True)
    edad = Column(Integer, nullable=True)  # Edad en años
    fecha_nacimiento = Column(Date, nullable=True)
    sexo = Column(String(10), nullable=True)  # Macho, Hembra
    color = Column(String(50), nullable=True)
    peso = Column(Float, nullable=True)  # Peso en kg
    observaciones = Column(String(500), nullable=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Clave foránea
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="mascotas")
    
    def __repr__(self):
        return f"<Mascota {self.nombre} - {self.especie}>"
