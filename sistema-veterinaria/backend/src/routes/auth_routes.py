"""
Rutas para autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from src.config.database import get_db
from src.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    Token,
    LoginRequest
)
from src.controllers.auth_controller import AuthController
from src.middleware.auth import get_current_user, require_admin
from src.models.usuario import Usuario

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en el sistema
    """
    return AuthController.register(db, usuario)


@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica un usuario y retorna un token JWT
    """
    return AuthController.login(db, login_data)


@router.post("/login-form", response_model=Token)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login compatible con OAuth2PasswordRequestForm (para Swagger UI)
    """
    login_data = LoginRequest(username=form_data.username, password=form_data.password)
    return AuthController.login(db, login_data)


@router.get("/me", response_model=UsuarioResponse)
def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    """
    Obtiene la información del usuario autenticado actualmente
    """
    return current_user


@router.get("/users", response_model=List[UsuarioResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Obtiene todos los usuarios (solo administradores)
    """
    return AuthController.get_all_users(db, skip, limit)


@router.get("/users/{user_id}", response_model=UsuarioResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Obtiene un usuario por ID (solo administradores)
    """
    return AuthController.get_user_by_id(db, user_id)


@router.put("/users/{user_id}", response_model=UsuarioResponse)
def update_user(
    user_id: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Actualiza un usuario (solo administradores)
    """
    return AuthController.update_user(db, user_id, usuario)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Elimina un usuario (solo administradores)
    """
    return AuthController.delete_user(db, user_id)
