"""
Rutas para gestión de productos
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.config.database import get_db
from src.schemas.producto_schema import (
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse
)
from src.controllers.producto_controller import ProductoController
from src.middleware.auth import get_current_user
from src.models.usuario import Usuario

router = APIRouter(prefix="/api/productos", tags=["Productos"])


@router.post("", response_model=ProductoResponse, status_code=201)
def create_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea un nuevo producto
    """
    return ProductoController.create(db, producto)


@router.get("", response_model=List[ProductoResponse])
def get_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    categoria: Optional[str] = None,
    activo: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene todos los productos con filtros opcionales
    """
    return ProductoController.get_all(db, skip, limit, categoria, activo, search)


@router.get("/low-stock", response_model=List[ProductoResponse])
def get_low_stock_productos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene productos con stock bajo
    """
    return ProductoController.get_low_stock(db)


@router.get("/codigo/{codigo}", response_model=ProductoResponse)
def get_producto_by_codigo(
    codigo: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene un producto por código
    """
    return ProductoController.get_by_codigo(db, codigo)


@router.get("/{producto_id}", response_model=ProductoResponse)
def get_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene un producto por ID
    """
    return ProductoController.get_by_id(db, producto_id)


@router.put("/{producto_id}", response_model=ProductoResponse)
def update_producto(
    producto_id: int,
    producto: ProductoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualiza un producto
    """
    return ProductoController.update(db, producto_id, producto)


@router.patch("/{producto_id}/stock", response_model=ProductoResponse)
def update_stock(
    producto_id: int,
    cantidad: int = Query(..., description="Cantidad a agregar (positivo) o restar (negativo)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualiza el stock de un producto
    """
    return ProductoController.update_stock(db, producto_id, cantidad)


@router.delete("/{producto_id}")
def delete_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Desactiva un producto
    """
    return ProductoController.delete(db, producto_id)
