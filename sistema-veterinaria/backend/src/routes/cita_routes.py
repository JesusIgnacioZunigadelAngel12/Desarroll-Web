"""
Rutas para gestión de citas
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from src.config.database import get_db
from src.schemas.cita_schema import CitaCreate, CitaUpdate, CitaResponse
from src.controllers.cita_controller import CitaController
from src.middleware.auth import get_current_user
from src.models.usuario import Usuario

router = APIRouter(prefix="/api/citas", tags=["Citas"])


@router.get("/disponibilidad")
def check_disponibilidad(
    veterinario: str,
    fecha_hora:  datetime,
    exclude_id:  Optional[int] = None,
    db:          Session       = Depends(get_db),
    _:           Usuario       = Depends(get_current_user)
):
    """Comprueba si un veterinario está disponible en un horario."""
    return CitaController.check_disponibilidad(db, veterinario, fecha_hora, exclude_id)


@router.get("", response_model=List[CitaResponse])
def get_citas(
    skip:       int            = Query(0, ge=0),
    limit:      int            = Query(200, ge=1, le=500),
    estado:     Optional[str]  = None,
    cliente_id: Optional[int]  = None,
    db:         Session        = Depends(get_db),
    _:          Usuario        = Depends(get_current_user)
):
    return CitaController.get_all(db, skip, limit, estado, cliente_id)


@router.post("", response_model=CitaResponse, status_code=201)
def create_cita(
    cita: CitaCreate,
    db:   Session = Depends(get_db),
    _:    Usuario = Depends(get_current_user)
):
    return CitaController.create(db, cita)


@router.get("/{cita_id}", response_model=CitaResponse)
def get_cita(
    cita_id: int,
    db:      Session = Depends(get_db),
    _:       Usuario = Depends(get_current_user)
):
    return CitaController.get_by_id(db, cita_id)


@router.put("/{cita_id}", response_model=CitaResponse)
def update_cita(
    cita_id: int,
    cita:    CitaUpdate,
    db:      Session = Depends(get_db),
    _:       Usuario = Depends(get_current_user)
):
    return CitaController.update(db, cita_id, cita)


@router.delete("/{cita_id}")
def delete_cita(
    cita_id: int,
    db:      Session = Depends(get_db),
    _:       Usuario = Depends(get_current_user)
):
    return CitaController.delete(db, cita_id)
