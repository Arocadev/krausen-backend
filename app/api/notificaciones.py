from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.base import get_db
from app.models.usuario import Usuario
from app.models.notificacion import Notificacion
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/notificaciones", tags=["Notificaciones"])

def notificacion_a_dict(n: Notificacion):
    return {
        "id": n.id,
        "tipo": n.tipo,
        "leida": n.leida,
        "created_at": n.created_at.isoformat(),
        "cerveza_id": n.cerveza_id,
        "cerveza_nombre": n.cerveza.nombre if n.cerveza else None,
        "actor_username": n.actor.username if n.actor else None,
    }

@router.get("/")
def listar_notificaciones(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    notificaciones = (
        db.query(Notificacion)
        .options(joinedload(Notificacion.actor), joinedload(Notificacion.cerveza))
        .filter(Notificacion.usuario_id == current_user.id)
        .order_by(Notificacion.created_at.desc())
        .limit(30)
        .all()
    )
    no_leidas = sum(1 for n in notificaciones if not n.leida)
    return {
        "notificaciones": [notificacion_a_dict(n) for n in notificaciones],
        "no_leidas": no_leidas
    }

@router.patch("/leer-todas")
def marcar_todas_leidas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    db.query(Notificacion).filter(
        Notificacion.usuario_id == current_user.id,
        Notificacion.leida == False
    ).update({"leida": True})
    db.commit()
    return {"ok": True}

@router.patch("/{notificacion_id}/leer")
def marcar_leida(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    n = db.query(Notificacion).filter(
        Notificacion.id == notificacion_id,
        Notificacion.usuario_id == current_user.id
    ).first()
    if not n:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    n.leida = True
    db.commit()
    return {"ok": True}