from sqlalchemy.orm import Session
from src.models.veterinario import Veterinario
from src.schemas.veterinario_schema import VeterinarioCreate, VeterinarioUpdate

def get_all(db: Session, solo_activos: bool = False):
    q = db.query(Veterinario)
    if solo_activos:
        q = q.filter(Veterinario.activo == True)
    return q.order_by(Veterinario.apellido, Veterinario.nombre).all()

def get_by_id(db: Session, vet_id: int):
    return db.query(Veterinario).filter(Veterinario.id == vet_id).first()

def create(db: Session, data: VeterinarioCreate):
    vet = Veterinario(**data.model_dump())
    db.add(vet); db.commit(); db.refresh(vet)
    return vet

def update(db: Session, vet_id: int, data: VeterinarioUpdate):
    vet = get_by_id(db, vet_id)
    if not vet: return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(vet, k, v)
    db.commit(); db.refresh(vet)
    return vet

def delete(db: Session, vet_id: int):
    vet = get_by_id(db, vet_id)
    if not vet: return False
    db.delete(vet); db.commit()
    return True
