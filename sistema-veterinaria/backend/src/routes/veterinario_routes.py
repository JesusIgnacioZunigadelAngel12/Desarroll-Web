from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.config.database import get_db
from src.schemas.veterinario_schema import VeterinarioCreate, VeterinarioUpdate, VeterinarioResponse
from src.controllers import veterinario_controller
from src.middleware.auth import get_current_user
from src.models.usuario import Usuario

router = APIRouter(prefix="/api/veterinarios", tags=["Veterinarios"])

@router.get("", response_model=List[VeterinarioResponse])
def list_veterinarios(solo_activos: bool = False, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)):
    return veterinario_controller.get_all(db, solo_activos)

@router.get("/{vet_id}", response_model=VeterinarioResponse)
def get_veterinario(vet_id: int, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)):
    v = veterinario_controller.get_by_id(db, vet_id)
    if not v: raise HTTPException(404, "Veterinario no encontrado")
    return v

@router.post("", response_model=VeterinarioResponse, status_code=201)
def create_veterinario(data: VeterinarioCreate, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)):
    return veterinario_controller.create(db, data)

@router.put("/{vet_id}", response_model=VeterinarioResponse)
def update_veterinario(vet_id: int, data: VeterinarioUpdate, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)):
    v = veterinario_controller.update(db, vet_id, data)
    if not v: raise HTTPException(404, "Veterinario no encontrado")
    return v

@router.delete("/{vet_id}")
def delete_veterinario(vet_id: int, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)):
    if not veterinario_controller.delete(db, vet_id):
        raise HTTPException(404, "Veterinario no encontrado")
    return {"message": "Veterinario eliminado"}
