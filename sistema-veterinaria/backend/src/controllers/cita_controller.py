"""
Controlador de Citas
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.cita import Cita
from src.schemas.cita_schema import CitaCreate, CitaUpdate
from typing import Optional
from datetime import datetime, timedelta


SLOT_MINUTOS = 30  # duración mínima de una cita en minutos


class CitaController:

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 200,
                estado: Optional[str] = None, cliente_id: Optional[int] = None):
        q = db.query(Cita)
        if estado:
            q = q.filter(Cita.estado == estado)
        if cliente_id:
            q = q.filter(Cita.cliente_id == cliente_id)
        return q.order_by(Cita.fecha_hora).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, cita_id: int):
        cita = db.query(Cita).filter(Cita.id == cita_id).first()
        if not cita:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return cita

    @staticmethod
    def _conflicto(db: Session, veterinario: str, fecha_hora: datetime,
                   exclude_id: Optional[int] = None):
        """Devuelve la cita en conflicto o None si el horario está libre.
        Considera conflicto cuando existe una cita del mismo veterinario
        dentro del rango (fecha_hora - SLOT, fecha_hora + SLOT), excluyendo canceladas."""
        if not veterinario:
            return None
        ventana = timedelta(minutes=SLOT_MINUTOS)
        q = db.query(Cita).filter(
            Cita.veterinario == veterinario,
            Cita.estado != "cancelada",
            Cita.fecha_hora >= fecha_hora - ventana,
            Cita.fecha_hora <  fecha_hora + ventana,
        )
        if exclude_id:
            q = q.filter(Cita.id != exclude_id)
        return q.first()

    @staticmethod
    def check_disponibilidad(db: Session, veterinario: str, fecha_hora: datetime,
                             exclude_id: Optional[int] = None):
        conflicto = CitaController._conflicto(db, veterinario, fecha_hora, exclude_id)
        if conflicto:
            return {
                "disponible": False,
                "mensaje": f"El veterinario ya tiene una cita a las "
                           f"{conflicto.fecha_hora.strftime('%H:%M')} "
                           f"(ID #{conflicto.id} — {conflicto.estado})"
            }
        return {"disponible": True, "mensaje": "Horario disponible"}

    @staticmethod
    def create(db: Session, data: CitaCreate):
        if data.veterinario:
            conflicto = CitaController._conflicto(db, data.veterinario, data.fecha_hora)
            if conflicto:
                raise HTTPException(
                    status_code=409,
                    detail=f"Conflicto de horario: {data.veterinario} ya tiene una cita "
                           f"a las {conflicto.fecha_hora.strftime('%H:%M')} (ID #{conflicto.id})"
                )
        cita = Cita(**data.model_dump())
        db.add(cita)
        db.commit()
        db.refresh(cita)
        return cita

    @staticmethod
    def update(db: Session, cita_id: int, data: CitaUpdate):
        cita = CitaController.get_by_id(db, cita_id)
        nueva_fecha = data.fecha_hora if data.fecha_hora else cita.fecha_hora
        nuevo_vet   = data.veterinario if data.veterinario is not None else cita.veterinario
        if nuevo_vet:
            conflicto = CitaController._conflicto(db, nuevo_vet, nueva_fecha, exclude_id=cita_id)
            if conflicto:
                raise HTTPException(
                    status_code=409,
                    detail=f"Conflicto de horario: {nuevo_vet} ya tiene una cita "
                           f"a las {conflicto.fecha_hora.strftime('%H:%M')} (ID #{conflicto.id})"
                )
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(cita, field, value)
        db.commit()
        db.refresh(cita)
        return cita

    @staticmethod
    def delete(db: Session, cita_id: int):
        cita = CitaController.get_by_id(db, cita_id)
        db.delete(cita)
        db.commit()
        return {"message": "Cita eliminada"}
