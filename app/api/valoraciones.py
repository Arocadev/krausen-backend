from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.base import get_db
from app.models.usuario import Usuario
from app.schemas.valoracion import ValoracionCreate, ValoracionResponse
from app.services.valoracion_service import crear_valoracion, obtener_valoraciones, obtener_media, eliminar_valoracion
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/cervezas", tags=["Valoraciones"])

@router.get("/{cerveza_id}/valoraciones", response_model=List[ValoracionResponse])
def listar_valoraciones(cerveza_id: int, db: Session = Depends(get_db)):
    return obtener_valoraciones(db, cerveza_id)

@router.get("/{cerveza_id}/media")
def media_valoraciones(cerveza_id: int, db: Session = Depends(get_db)):
    return {"media": obtener_media(db, cerveza_id)}

@router.post("/{cerveza_id}/valoraciones", response_model=ValoracionResponse, status_code=201)
def nueva_valoracion(
    cerveza_id: int,
    datos: ValoracionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return crear_valoracion(db, cerveza_id, current_user.id, datos)

@router.delete("/{cerveza_id}/valoraciones/{valoracion_id}", status_code=204)
def borrar_valoracion(
    cerveza_id: int,
    valoracion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    eliminar_valoracion(db, valoracion_id, current_user.id)