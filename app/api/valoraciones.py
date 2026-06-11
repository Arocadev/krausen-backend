from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.models.usuario import Usuario
from app.services.valoracion_service import dar_me_gusta, quitar_me_gusta, contar_me_gustas, usuario_dio_me_gusta
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/cervezas", tags=["Me gusta"])

@router.get("/{cerveza_id}/me-gusta")
def info_me_gusta(cerveza_id: int, db: Session = Depends(get_db)):
    total = contar_me_gustas(db, cerveza_id)
    return {"total": total}

@router.get("/{cerveza_id}/me-gusta/estado")
def estado_me_gusta(
    cerveza_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    dado = usuario_dio_me_gusta(db, cerveza_id, current_user.id)
    total = contar_me_gustas(db, cerveza_id)
    return {"dado": dado, "total": total}

@router.post("/{cerveza_id}/me-gusta", status_code=201)
def like(
    cerveza_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return dar_me_gusta(db, cerveza_id, current_user.id)

@router.delete("/{cerveza_id}/me-gusta")
def unlike(
    cerveza_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return quitar_me_gusta(db, cerveza_id, current_user.id)