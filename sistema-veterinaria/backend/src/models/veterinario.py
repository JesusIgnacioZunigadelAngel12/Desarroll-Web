from sqlalchemy import Column, Integer, String, Boolean
from src.config.database import Base

class Veterinario(Base):
    __tablename__ = 'veterinarios'

    id           = Column(Integer, primary_key=True, index=True)
    nombre       = Column(String(100), nullable=False)
    apellido     = Column(String(100), nullable=False)
    especialidad = Column(String(150), nullable=True)
    telefono     = Column(String(20), nullable=True)
    email        = Column(String(150), nullable=True)
    activo       = Column(Boolean, default=True)
