"""
Controlador para gestión de clientes
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from src.models.cliente import Cliente
from src.schemas.cliente_schema import ClienteCreate, ClienteUpdate


class ClienteController:
    """Controlador para operaciones CRUD de clientes"""
    
    @staticmethod
    def create(db: Session, cliente: ClienteCreate) -> Cliente:
        """
        Crea un nuevo cliente
        
        Args:
            db: Sesión de base de datos
            cliente: Datos del cliente a crear
        
        Returns:
            Cliente creado
        
        Raises:
            HTTPException: Si el email o documento ya existen
        """
        # Verificar email único si se proporciona
        if cliente.email:
            existing_email = db.query(Cliente).filter(Cliente.email == cliente.email).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )
        
        # Verificar documento único si se proporciona
        if cliente.documento:
            existing_doc = db.query(Cliente).filter(Cliente.documento == cliente.documento).first()
            if existing_doc:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El documento ya está registrado"
                )
        
        db_cliente = Cliente(**cliente.model_dump())
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        
        return db_cliente
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[Cliente]:
        """
        Obtiene todos los clientes con paginación y búsqueda opcional
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            search: Término de búsqueda (nombre, apellido o email)
        
        Returns:
            Lista de clientes
        """
        query = db.query(Cliente)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Cliente.nombre.ilike(search_filter)) |
                (Cliente.apellido.ilike(search_filter)) |
                (Cliente.email.ilike(search_filter)) |
                (Cliente.telefono.ilike(search_filter))
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, cliente_id: int) -> Cliente:
        """
        Obtiene un cliente por ID
        
        Args:
            db: Sesión de base de datos
            cliente_id: ID del cliente
        
        Returns:
            Cliente encontrado
        
        Raises:
            HTTPException: Si el cliente no existe
        """
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        return cliente
    
    @staticmethod
    def update(db: Session, cliente_id: int, cliente: ClienteUpdate) -> Cliente:
        """
        Actualiza un cliente
        
        Args:
            db: Sesión de base de datos
            cliente_id: ID del cliente
            cliente: Datos a actualizar
        
        Returns:
            Cliente actualizado
        """
        db_cliente = ClienteController.get_by_id(db, cliente_id)
        
        update_data = cliente.model_dump(exclude_unset=True)
        
        # Verificar email único si se actualiza
        if "email" in update_data and update_data["email"]:
            existing = db.query(Cliente).filter(
                Cliente.email == update_data["email"],
                Cliente.id != cliente_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )
        
        # Verificar documento único si se actualiza
        if "documento" in update_data and update_data["documento"]:
            existing = db.query(Cliente).filter(
                Cliente.documento == update_data["documento"],
                Cliente.id != cliente_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El documento ya está registrado"
                )
        
        for field, value in update_data.items():
            setattr(db_cliente, field, value)
        
        db.commit()
        db.refresh(db_cliente)
        
        return db_cliente
    
    @staticmethod
    def delete(db: Session, cliente_id: int) -> dict:
        """
        Elimina un cliente
        
        Args:
            db: Sesión de base de datos
            cliente_id: ID del cliente
        
        Returns:
            Mensaje de confirmación
        """
        db_cliente = ClienteController.get_by_id(db, cliente_id)
        
        db.delete(db_cliente)
        db.commit()
        
        return {"message": "Cliente eliminado correctamente"}
