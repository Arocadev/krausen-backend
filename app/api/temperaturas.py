from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.models.base import get_db
from app.models.usuario import Usuario
from app.models.cerveza import Cerveza
from app.models.temperatura import RegistroTemperatura
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/cervezas", tags=["Temperaturas"])

class TemperaturaInput(BaseModel):
    slot: int
    temperatura: float

class TemperaturaResponse(BaseModel):
    id: int
    slot: int
    temperatura: float
    class Config:
        from_attributes = True

@router.get("/{cerveza_id}/temperaturas", response_model=List[TemperaturaResponse])
def obtener_temperaturas(cerveza_id: int, db: Session = Depends(get_db)):
    return db.query(RegistroTemperatura).filter(
        RegistroTemperatura.cerveza_id == cerveza_id
    ).order_by(RegistroTemperatura.slot).all()

@router.post("/{cerveza_id}/temperaturas", status_code=201)
def registrar_temperatura(
    cerveza_id: int,
    datos: TemperaturaInput,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    cerveza = db.query(Cerveza).filter(Cerveza.id == cerveza_id).first()
    if not cerveza:
        raise HTTPException(status_code=404, detail="Cerveza no encontrada")
    if cerveza.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Solo el autor puede registrar temperaturas")
    if not cerveza.dias_fermentacion or not cerveza.intervalo_horas:
        raise HTTPException(status_code=400, detail="Esta receta no tiene fermentación configurada")

    total_slots = (cerveza.dias_fermentacion * 24) // cerveza.intervalo_horas
    if datos.slot < 0 or datos.slot >= total_slots:
        raise HTTPException(status_code=400, detail=f"El slot debe estar entre 0 y {total_slots - 1}")

    existente = db.query(RegistroTemperatura).filter(
        RegistroTemperatura.cerveza_id == cerveza_id,
        RegistroTemperatura.slot == datos.slot
    ).first()

    if existente:
        existente.temperatura = datos.temperatura
    else:
        db.add(RegistroTemperatura(
            cerveza_id=cerveza_id,
            slot=datos.slot,
            temperatura=datos.temperatura
        ))

    db.commit()
    return {"mensaje": "Temperatura registrada"}

@router.get("/{cerveza_id}/fermentacion")
def info_fermentacion(cerveza_id: int, db: Session = Depends(get_db)):
    cerveza = db.query(Cerveza).filter(Cerveza.id == cerveza_id).first()
    if not cerveza:
        raise HTTPException(status_code=404, detail="Cerveza no encontrada")
    if not cerveza.dias_fermentacion:
        return {"configurada": False}
    total_slots = (cerveza.dias_fermentacion * 24) // cerveza.intervalo_horas
    registrados = db.query(RegistroTemperatura).filter(
        RegistroTemperatura.cerveza_id == cerveza_id
    ).count()
    return {
        "configurada": True,
        "dias": cerveza.dias_fermentacion,
        "intervalo_horas": cerveza.intervalo_horas,
        "total_slots": total_slots,
        "registrados": registrados
    }