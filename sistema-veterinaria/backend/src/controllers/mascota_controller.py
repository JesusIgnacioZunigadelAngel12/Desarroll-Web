"""
Controlador para gestión de mascotas
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from src.models.mascota import Mascota
from src.models.cliente import Cliente
from src.schemas.mascota_schema import MascotaCreate, MascotaUpdate


class MascotaController:
    """Controlador para operaciones CRUD de mascotas"""
    
    @staticmethod
    def create(db: Session, mascota: MascotaCreate) -> Mascota:
        """
        Crea una nueva mascota
        
        Args:
            db: Sesión de base de datos
            mascota: Datos de la mascota a crear
        
        Returns:
            Mascota creada
        
        Raises:
            HTTPException: Si el cliente no existe
        """
        # Verificar que el cliente existe
        cliente = db.query(Cliente).filter(Cliente.id == mascota.cliente_id).first()
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        db_mascota = Mascota(**mascota.model_dump())
        db.add(db_mascota)
        db.commit()
        db.refresh(db_mascota)
        
        return db_mascota
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        cliente_id: Optional[int] = None
    ) -> List[Mascota]:
        """
        Obtiene todas las mascotas con filtro opcional por cliente
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            cliente_id: ID del cliente para filtrar
        
        Returns:
            Lista de mascotas
        """
        query = db.query(Mascota)
        
        if cliente_id:
            query = query.filter(Mascota.cliente_id == cliente_id)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, mascota_id: int) -> Mascota:
        """
        Obtiene una mascota por ID
        
        Args:
            db: Sesión de base de datos
            mascota_id: ID de la mascota
        
        Returns:
            Mascota encontrada
        
        Raises:
            HTTPException: Si la mascota no existe
        """
        mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
        
        if not mascota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mascota no encontrada"
            )
        
        return mascota
    
    @staticmethod
    def get_by_cliente(db: Session, cliente_id: int) -> List[Mascota]:
        """
        Obtiene todas las mascotas de un cliente
        
        Args:
            db: Sesión de base de datos
            cliente_id: ID del cliente
        
        Returns:
            Lista de mascotas del cliente
        """
        return db.query(Mascota).filter(Mascota.cliente_id == cliente_id).all()
    
    @staticmethod
    def update(db: Session, mascota_id: int, mascota: MascotaUpdate) -> Mascota:
        """
        Actualiza una mascota
        
        Args:
            db: Sesión de base de datos
            mascota_id: ID de la mascota
            mascota: Datos a actualizar
        
        Returns:
            Mascota actualizada
        """
        db_mascota = MascotaController.get_by_id(db, mascota_id)
        
        update_data = mascota.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_mascota, field, value)
        
        db.commit()
        db.refresh(db_mascota)
        
        return db_mascota
    
    @staticmethod
    def delete(db: Session, mascota_id: int) -> dict:
        """
        Elimina una mascota
        
        Args:
            db: Sesión de base de datos
            mascota_id: ID de la mascota
        
        Returns:
            Mensaje de confirmación
        """
        db_mascota = MascotaController.get_by_id(db, mascota_id)
        
        db.delete(db_mascota)
        db.commit()
        
        return {"message": "Mascota eliminada correctamente"}
