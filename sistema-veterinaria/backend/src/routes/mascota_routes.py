"""
Rutas para gestión de mascotas
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.config.database import get_db
from src.schemas.mascota_schema import (
    MascotaCreate,
    MascotaUpdate,
    MascotaResponse
)
from src.controllers.mascota_controller import MascotaController
from src.middleware.auth import get_current_user
from src.models.usuario import Usuario

router = APIRouter(prefix="/api/mascotas", tags=["Mascotas"])


@router.post("", response_model=MascotaResponse, status_code=201)
def create_mascota(
    mascota: MascotaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea una nueva mascota
    """
    return MascotaController.create(db, mascota)


@router.get("", response_model=List[MascotaResponse])
def get_mascotas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    cliente_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene todas las mascotas con filtro opcional por cliente
    """
    return MascotaController.get_all(db, skip, limit, cliente_id)


@router.get("/cliente/{cliente_id}", response_model=List[MascotaResponse])
def get_mascotas_by_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene todas las mascotas de un cliente específico
    """
    return MascotaController.get_by_cliente(db, cliente_id)


@router.get("/{mascota_id}", response_model=MascotaResponse)
def get_mascota(
    mascota_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene una mascota por ID
    """
    return MascotaController.get_by_id(db, mascota_id)


@router.put("/{mascota_id}", response_model=MascotaResponse)
def update_mascota(
    mascota_id: int,
    mascota: MascotaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualiza una mascota
    """
    return MascotaController.update(db, mascota_id, mascota)


@router.delete("/{mascota_id}")
def delete_mascota(
    mascota_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Elimina una mascota
    """
    return MascotaController.delete(db, mascota_id)
