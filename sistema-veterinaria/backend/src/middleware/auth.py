"""
Utilidades para autenticación JWT y hashing de contraseñas
"""
from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.config.settings import settings
from src.config.database import get_db
from src.models.usuario import Usuario
from src.schemas.usuario_schema import TokenData

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que una contraseña coincida con su hash
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Contraseña hasheada
    
    Returns:
        True si coinciden, False en caso contrario
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    """
    Genera un hash de la contraseña
    
    Args:
        password: Contraseña en texto plano
    
    Returns:
        Hash de la contraseña
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT de acceso
    
    Args:
        data: Datos a incluir en el token
        expires_delta: Tiempo de expiración personalizado
    
    Returns:
        Token JWT generado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def authenticate_user(db: Session, username: str, password: str) -> Optional[Usuario]:
    """
    Autentica un usuario verificando sus credenciales
    
    Args:
        db: Sesión de base de datos
        username: Nombre de usuario
        password: Contraseña
    
    Returns:
        Usuario si las credenciales son correctas, None en caso contrario
    """
    user = db.query(Usuario).filter(Usuario.username == username).first()
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Obtiene el usuario actual desde el token JWT
    
    Args:
        token: Token JWT
        db: Sesión de base de datos
    
    Returns:
        Usuario actual
    
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = db.query(Usuario).filter(Usuario.username == token_data.username).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return user


async def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Verifica que el usuario actual esté activo
    
    Args:
        current_user: Usuario actual
    
    Returns:
        Usuario si está activo
    
    Raises:
        HTTPException: Si el usuario está inactivo
    """
    if not current_user.activo:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    return current_user


def require_admin(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """
    Verifica que el usuario actual tenga rol de administrador
    
    Args:
        current_user: Usuario actual
    
    Returns:
        Usuario si es administrador
    
    Raises:
        HTTPException: Si el usuario no es administrador
    """
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos suficientes"
        )
    
    return current_user
