from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.base import get_db
from app.models.usuario import Usuario
from app.models.cerveza import Cerveza
from app.models.notificacion import Notificacion
from app.models.valoracion import MeGusta
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/cervezas", tags=["Me gusta"])

@router.get("/{cerveza_id}/me-gusta")
def info_me_gusta(cerveza_id: int, db: Session = Depends(get_db)):
    total = db.query(func.count(MeGusta.id)).filter(MeGusta.cerveza_id == cerveza_id).scalar()
    return {"total": total}

@router.get("/{cerveza_id}/me-gusta/estado")
def estado_me_gusta(
    cerveza_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    resultado = db.query(
        func.count(MeGusta.id).label("total"),
        func.bool_or(MeGusta.usuario_id == current_user.id).label("dado")
    ).filter(MeGusta.cerveza_id == cerveza_id).one()

    return {"dado": resultado.dado or False, "total": resultado.total}

@router.post("/{cerveza_id}/me-gusta", status_code=201)
def like(
    cerveza_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    cerveza = db.query(Cerveza).filter(Cerveza.id == cerveza_id).first()
    if not cerveza:
        raise HTTPException(status_code=404, detail="Cerveza no encontrada")
    if cerveza.usuario_id == current_user.id:
        raise HTTPException(status_code=403, detail="No puedes dar me gusta a tu propia cerveza")

    existente = db.query(MeGusta).filter(
        MeGusta.cerveza_id == cerveza_id,
        MeGusta.usuario_id == current_user.id
    ).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ya has dado me gusta a esta cerveza")

    db.add(MeGusta(cerveza_id=cerveza_id, usuario_id=current_user.id))

    ya_existe_notif = db.query(Notificacion).filter(
        Notificacion.usuario_id == cerveza.usuario_id,
        Notificacion.actor_id == current_user.id,
        Notificacion.tipo == "like",
        Notificacion.cerveza_id == cerveza_id
    ).first()
    if not ya_existe_notif:
        db.add(Notificacion(
            usuario_id=cerveza.usuario_id,
            actor_id=current_user.id,
            tipo="like",
            cerveza_id=cerveza_id
        ))

    db.commit()
    return {"mensaje": "Me gusta añadido"}

@router.delete("/{cerveza_id}/me-gusta")
def unlike(
    cerveza_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    existente = db.query(MeGusta).filter(
        MeGusta.cerveza_id == cerveza_id,
        MeGusta.usuario_id == current_user.id
    ).first()
    if not existente:
        raise HTTPException(status_code=404, detail="No has dado me gusta a esta cerveza")
    db.delete(existente)
    db.commit()
    return {"mensaje": "Me gusta eliminado"}