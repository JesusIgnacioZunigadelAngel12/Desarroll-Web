"""
Controlador para gestión de ventas (POS)
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from datetime import datetime, date
import random
import string

from src.models.venta import Venta, DetalleVenta
from src.models.producto import Producto
from src.models.cliente import Cliente
from src.schemas.venta_schema import VentaCreate, VentaStats
from src.controllers.producto_controller import ProductoController


class VentaController:
    """Controlador para operaciones de ventas (POS)"""
    
    @staticmethod
    def generate_codigo_venta() -> str:
        """
        Genera un código único para la venta
        
        Returns:
            Código de venta generado
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"V-{timestamp}-{random_str}"
    
    @staticmethod
    def create(db: Session, venta: VentaCreate, usuario_id: int) -> Venta:
        """
        Crea una nueva venta y actualiza el inventario
        
        Args:
            db: Sesión de base de datos
            venta: Datos de la venta
            usuario_id: ID del usuario que realiza la venta
        
        Returns:
            Venta creada
        
        Raises:
            HTTPException: Si hay stock insuficiente o datos inválidos
        """
        # Verificar que el cliente existe si se proporciona
        if venta.cliente_id:
            cliente = db.query(Cliente).filter(Cliente.id == venta.cliente_id).first()
            if not cliente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cliente no encontrado"
                )
        
        # Validar y calcular totales
        subtotal = 0.0
        detalles_venta = []
        
        for detalle in venta.detalles:
            # Obtener producto
            producto = ProductoController.get_by_id(db, detalle.producto_id)
            
            # Verificar stock disponible
            if producto.stock < detalle.cantidad:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}"
                )
            
            # Calcular subtotal del detalle
            subtotal_detalle = detalle.cantidad * detalle.precio_unitario
            subtotal += subtotal_detalle
            
            # Crear detalle de venta
            detalles_venta.append({
                "producto_id": detalle.producto_id,
                "cantidad": detalle.cantidad,
                "precio_unitario": detalle.precio_unitario,
                "subtotal": subtotal_detalle
            })
            
            # Actualizar stock del producto
            producto.stock -= detalle.cantidad
        
        # Calcular total con descuento
        total = subtotal - venta.descuento
        
        if total < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El descuento no puede ser mayor al subtotal"
            )
        
        # Crear venta
        db_venta = Venta(
            codigo_venta=VentaController.generate_codigo_venta(),
            cliente_id=venta.cliente_id,
            usuario_id=usuario_id,
            subtotal=subtotal,
            descuento=venta.descuento,
            total=total,
            metodo_pago=venta.metodo_pago,
            notas=venta.notas
        )
        
        db.add(db_venta)
        db.flush()  # Obtener el ID de la venta
        
        # Agregar detalles de venta
        for detalle_data in detalles_venta:
            detalle = DetalleVenta(
                venta_id=db_venta.id,
                **detalle_data
            )
            db.add(detalle)
        
        db.commit()
        db.refresh(db_venta)
        
        return db_venta
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        cliente_id: int = None,
        fecha_inicio: date = None,
        fecha_fin: date = None
    ) -> List[Venta]:
        """
        Obtiene todas las ventas con filtros opcionales
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            cliente_id: Filtrar por cliente
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango
        
        Returns:
            Lista de ventas
        """
        query = db.query(Venta)
        
        if cliente_id:
            query = query.filter(Venta.cliente_id == cliente_id)
        
        if fecha_inicio:
            query = query.filter(Venta.fecha >= fecha_inicio)
        
        if fecha_fin:
            # Incluir todo el día final
            fecha_fin_completa = datetime.combine(fecha_fin, datetime.max.time())
            query = query.filter(Venta.fecha <= fecha_fin_completa)
        
        return query.order_by(Venta.fecha.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, venta_id: int) -> Venta:
        """
        Obtiene una venta por ID con sus detalles
        
        Args:
            db: Sesión de base de datos
            venta_id: ID de la venta
        
        Returns:
            Venta encontrada
        
        Raises:
            HTTPException: Si la venta no existe
        """
        venta = db.query(Venta).filter(Venta.id == venta_id).first()
        
        if not venta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venta no encontrada"
            )
        
        return venta
    
    @staticmethod
    def get_by_codigo(db: Session, codigo_venta: str) -> Venta:
        """
        Obtiene una venta por código
        
        Args:
            db: Sesión de base de datos
            codigo_venta: Código de la venta
        
        Returns:
            Venta encontrada
        
        Raises:
            HTTPException: Si la venta no existe
        """
        venta = db.query(Venta).filter(Venta.codigo_venta == codigo_venta).first()
        
        if not venta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venta no encontrada"
            )
        
        return venta
    
    @staticmethod
    def get_statistics(db: Session, fecha_inicio: date = None, fecha_fin: date = None) -> VentaStats:
        """
        Obtiene estadísticas de ventas
        
        Args:
            db: Sesión de base de datos
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango
        
        Returns:
            Estadísticas de ventas
        """
        query = db.query(Venta).filter(Venta.estado == "completada")
        
        if fecha_inicio:
            query = query.filter(Venta.fecha >= fecha_inicio)
        
        if fecha_fin:
            fecha_fin_completa = datetime.combine(fecha_fin, datetime.max.time())
            query = query.filter(Venta.fecha <= fecha_fin_completa)
        
        ventas = query.all()
        
        total_ventas = len(ventas)
        monto_total = sum(venta.total for venta in ventas)
        promedio_venta = monto_total / total_ventas if total_ventas > 0 else 0
        
        # Ventas de hoy
        hoy = date.today()
        ventas_hoy = [v for v in ventas if v.fecha.date() == hoy]
        total_ventas_hoy = len(ventas_hoy)
        monto_hoy = sum(venta.total for venta in ventas_hoy)
        
        return VentaStats(
            total_ventas=total_ventas,
            monto_total=monto_total,
            promedio_venta=promedio_venta,
            ventas_hoy=total_ventas_hoy,
            monto_hoy=monto_hoy
        )
    
    @staticmethod
    def cancel(db: Session, venta_id: int) -> Venta:
        """
        Cancela una venta y restaura el inventario
        
        Args:
            db: Sesión de base de datos
            venta_id: ID de la venta
        
        Returns:
            Venta cancelada
        
        Raises:
            HTTPException: Si la venta ya está cancelada
        """
        venta = VentaController.get_by_id(db, venta_id)
        
        if venta.estado == "cancelada":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La venta ya está cancelada"
            )
        
        # Restaurar inventario
        for detalle in venta.detalles:
            producto = ProductoController.get_by_id(db, detalle.producto_id)
            producto.stock += detalle.cantidad
        
        # Marcar venta como cancelada
        venta.estado = "cancelada"
        
        db.commit()
        db.refresh(venta)
        
        return venta
