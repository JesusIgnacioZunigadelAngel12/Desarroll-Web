from pydantic import BaseModel
from typing import Optional

class VeterinarioBase(BaseModel):
    nombre:       str
    apellido:     str
    especialidad: Optional[str] = None
    telefono:     Optional[str] = None
    email:        Optional[str] = None
    activo:       bool = True

class VeterinarioCreate(VeterinarioBase):
    pass

class VeterinarioUpdate(BaseModel):
    nombre:       Optional[str]  = None
    apellido:     Optional[str]  = None
    especialidad: Optional[str]  = None
    telefono:     Optional[str]  = None
    email:        Optional[str]  = None
    activo:       Optional[bool] = None

class VeterinarioResponse(VeterinarioBase):
    id: int

    model_config = {"from_attributes": True}
