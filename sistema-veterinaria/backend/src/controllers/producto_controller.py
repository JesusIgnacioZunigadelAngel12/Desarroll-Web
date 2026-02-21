"""
Controlador para gestión de productos
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from src.models.producto import Producto
from src.schemas.producto_schema import ProductoCreate, ProductoUpdate


class ProductoController:
    """Controlador para operaciones CRUD de productos"""
    
    @staticmethod
    def create(db: Session, producto: ProductoCreate) -> Producto:
        """
        Crea un nuevo producto
        
        Args:
            db: Sesión de base de datos
            producto: Datos del producto a crear
        
        Returns:
            Producto creado
        
        Raises:
            HTTPException: Si el código ya existe
        """
        # Verificar que el código sea único
        existing = db.query(Producto).filter(Producto.codigo == producto.codigo).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El código de producto ya existe"
            )
        
        db_producto = Producto(**producto.model_dump())
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        
        return db_producto
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        categoria: Optional[str] = None,
        activo: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[Producto]:
        """
        Obtiene todos los productos con filtros opcionales
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            categoria: Filtrar por categoría
            activo: Filtrar por estado activo
            search: Término de búsqueda (nombre, código o descripción)
        
        Returns:
            Lista de productos
        """
        query = db.query(Producto)
        
        if categoria:
            query = query.filter(Producto.categoria == categoria)
        
        if activo is not None:
            query = query.filter(Producto.activo == activo)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Producto.nombre.ilike(search_filter)) |
                (Producto.codigo.ilike(search_filter)) |
                (Producto.descripcion.ilike(search_filter))
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, producto_id: int) -> Producto:
        """
        Obtiene un producto por ID
        
        Args:
            db: Sesión de base de datos
            producto_id: ID del producto
        
        Returns:
            Producto encontrado
        
        Raises:
            HTTPException: Si el producto no existe
        """
        producto = db.query(Producto).filter(Producto.id == producto_id).first()
        
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        
        return producto
    
    @staticmethod
    def get_by_codigo(db: Session, codigo: str) -> Producto:
        """
        Obtiene un producto por código
        
        Args:
            db: Sesión de base de datos
            codigo: Código del producto
        
        Returns:
            Producto encontrado
        
        Raises:
            HTTPException: Si el producto no existe
        """
        producto = db.query(Producto).filter(Producto.codigo == codigo).first()
        
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        
        return producto
    
    @staticmethod
    def get_low_stock(db: Session) -> List[Producto]:
        """
        Obtiene productos con stock bajo (menor o igual al stock mínimo)
        
        Args:
            db: Sesión de base de datos
        
        Returns:
            Lista de productos con stock bajo
        """
        return db.query(Producto).filter(
            Producto.stock <= Producto.stock_minimo,
            Producto.activo == True
        ).all()
    
    @staticmethod
    def update(db: Session, producto_id: int, producto: ProductoUpdate) -> Producto:
        """
        Actualiza un producto
        
        Args:
            db: Sesión de base de datos
            producto_id: ID del producto
            producto: Datos a actualizar
        
        Returns:
            Producto actualizado
        """
        db_producto = ProductoController.get_by_id(db, producto_id)
        
        update_data = producto.model_dump(exclude_unset=True)
        
        # Verificar código único si se actualiza
        if "codigo" in update_data:
            existing = db.query(Producto).filter(
                Producto.codigo == update_data["codigo"],
                Producto.id != producto_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El código de producto ya existe"
                )
        
        for field, value in update_data.items():
            setattr(db_producto, field, value)
        
        db.commit()
        db.refresh(db_producto)
        
        return db_producto
    
    @staticmethod
    def update_stock(db: Session, producto_id: int, cantidad: int) -> Producto:
        """
        Actualiza el stock de un producto
        
        Args:
            db: Sesión de base de datos
            producto_id: ID del producto
            cantidad: Cantidad a agregar (positivo) o restar (negativo)
        
        Returns:
            Producto actualizado
        
        Raises:
            HTTPException: Si el stock resultante es negativo
        """
        db_producto = ProductoController.get_by_id(db, producto_id)
        
        nuevo_stock = db_producto.stock + cantidad
        
        if nuevo_stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock insuficiente"
            )
        
        db_producto.stock = nuevo_stock
        db.commit()
        db.refresh(db_producto)
        
        return db_producto
    
    @staticmethod
    def delete(db: Session, producto_id: int) -> dict:
        """
        Elimina un producto (desactivación lógica)
        
        Args:
            db: Sesión de base de datos
            producto_id: ID del producto
        
        Returns:
            Mensaje de confirmación
        """
        db_producto = ProductoController.get_by_id(db, producto_id)
        
        # Desactivar en lugar de eliminar
        db_producto.activo = False
        db.commit()
        
        return {"message": "Producto desactivado correctamente"}
