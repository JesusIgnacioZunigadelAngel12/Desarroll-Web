"""
Modelo de Cita (agenda veterinaria)
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from src.config.database import Base


class Cita(Base):
    __tablename__ = "citas"

    id              = Column(Integer, primary_key=True, index=True)
    cliente_id      = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    mascota_id      = Column(Integer, ForeignKey("mascotas.id"), nullable=False)
    fecha_hora      = Column(DateTime, nullable=False)
    motivo          = Column(String(200), nullable=False)
    estado          = Column(String(20), default="pendiente")   # pendiente | confirmada | completada | cancelada
    veterinario     = Column(String(100), nullable=True)
    notas           = Column(Text, nullable=True)
    fecha_creacion  = Column(DateTime, default=datetime.utcnow)

    cliente = relationship("Cliente", backref="citas")
    mascota = relationship("Mascota", backref="citas")
