"""
Rutas para gestión de clientes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.config.database import get_db
from src.schemas.cliente_schema import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteWithMascotas
)
from src.controllers.cliente_controller import ClienteController
from src.middleware.auth import get_current_user
from src.models.usuario import Usuario

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])


@router.post("", response_model=ClienteResponse, status_code=201)
def create_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea un nuevo cliente
    """
    return ClienteController.create(db, cliente)


@router.get("", response_model=List[ClienteResponse])
def get_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene todos los clientes con paginación y búsqueda opcional
    """
    return ClienteController.get_all(db, skip, limit, search)


@router.get("/{cliente_id}", response_model=ClienteWithMascotas)
def get_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene un cliente por ID incluyendo sus mascotas
    """
    return ClienteController.get_by_id(db, cliente_id)


@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualiza un cliente
    """
    return ClienteController.update(db, cliente_id, cliente)


@router.delete("/{cliente_id}")
def delete_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Elimina un cliente
    """
    return ClienteController.delete(db, cliente_id)
