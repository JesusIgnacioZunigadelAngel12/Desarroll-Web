"""
Rutas para gestión de ventas (POS)
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from src.config.database import get_db
from src.schemas.venta_schema import (
    VentaCreate,
    VentaResponse,
    VentaStats
)
from src.controllers.venta_controller import VentaController
from src.middleware.auth import get_current_user
from src.models.usuario import Usuario

router = APIRouter(prefix="/api/ventas", tags=["Ventas (POS)"])


@router.post("", response_model=VentaResponse, status_code=201)
def create_venta(
    venta: VentaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea una nueva venta y actualiza el inventario
    """
    return VentaController.create(db, venta, current_user.id)


@router.get("", response_model=List[VentaResponse])
def get_ventas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    cliente_id: Optional[int] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene todas las ventas con filtros opcionales
    """
    return VentaController.get_all(db, skip, limit, cliente_id, fecha_inicio, fecha_fin)


@router.get("/estadisticas", response_model=VentaStats)
def get_estadisticas(
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene estadísticas de ventas
    """
    return VentaController.get_statistics(db, fecha_inicio, fecha_fin)


@router.get("/codigo/{codigo_venta}", response_model=VentaResponse)
def get_venta_by_codigo(
    codigo_venta: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene una venta por código
    """
    return VentaController.get_by_codigo(db, codigo_venta)


@router.get("/{venta_id}", response_model=VentaResponse)
def get_venta(
    venta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene una venta por ID con sus detalles
    """
    return VentaController.get_by_id(db, venta_id)


@router.patch("/{venta_id}/cancelar", response_model=VentaResponse)
def cancel_venta(
    venta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cancela una venta y restaura el inventario
    """
    return VentaController.cancel(db, venta_id)
