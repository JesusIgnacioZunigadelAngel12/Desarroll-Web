"""
Controlador para autenticación de usuarios
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.models.usuario import Usuario
from src.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, LoginRequest, Token
from src.middleware.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token
)
from src.config.settings import settings


class AuthController:
    """Controlador para operaciones de autenticación"""
    
    @staticmethod
    def register(db: Session, usuario: UsuarioCreate) -> Usuario:
        """
        Registra un nuevo usuario
        
        Args:
            db: Sesión de base de datos
            usuario: Datos del usuario a crear
        
        Returns:
            Usuario creado
        
        Raises:
            HTTPException: Si el username o email ya existen
        """
        # Verificar si el username ya existe
        existing_user = db.query(Usuario).filter(Usuario.username == usuario.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El username ya está registrado"
            )
        
        # Verificar si el email ya existe
        existing_email = db.query(Usuario).filter(Usuario.email == usuario.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear usuario con contraseña hasheada
        hashed_password = get_password_hash(usuario.password)
        db_usuario = Usuario(
            username=usuario.username,
            email=usuario.email,
            hashed_password=hashed_password,
            nombre_completo=usuario.nombre_completo,
            rol=usuario.rol
        )
        
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        
        return db_usuario
    
    @staticmethod
    def login(db: Session, login_data: LoginRequest) -> Token:
        """
        Autentica un usuario y genera un token JWT
        
        Args:
            db: Sesión de base de datos
            login_data: Credenciales de login
        
        Returns:
            Token JWT
        
        Raises:
            HTTPException: Si las credenciales son incorrectas
        """
        user = authenticate_user(db, login_data.username, login_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Actualizar último acceso
        user.ultimo_acceso = datetime.utcnow()
        db.commit()
        
        # Crear token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
    
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        """Obtiene todos los usuarios"""
        return db.query(Usuario).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Usuario:
        """Obtiene un usuario por ID"""
        user = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return user
    
    @staticmethod
    def update_user(db: Session, user_id: int, usuario: UsuarioUpdate) -> Usuario:
        """Actualiza un usuario"""
        db_user = AuthController.get_user_by_id(db, user_id)
        
        update_data = usuario.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> dict:
        """Elimina un usuario"""
        db_user = AuthController.get_user_by_id(db, user_id)
        
        db.delete(db_user)
        db.commit()
        
        return {"message": "Usuario eliminado correctamente"}
