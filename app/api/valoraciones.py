from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.models.usuario import Usuario
from app.models.cerveza import Cerveza
from app.models.notificacion import Notificacion
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
    resultado = dar_me_gusta(db, cerveza_id, current_user.id)

    # Crear notificación al dueño de la cerveza (si no es el mismo usuario)
    cerveza = db.query(Cerveza).filter(Cerveza.id == cerveza_id).first()
    if cerveza and cerveza.usuario_id != current_user.id:
        ya_existe = db.query(Notificacion).filter(
            Notificacion.usuario_id == cerveza.usuario_id,
            Notificacion.actor_id == current_user.id,
            Notificacion.tipo == "like",
            Notificacion.cerveza_id == cerveza_id
        ).first()
        if not ya_existe:
            db.add(Notificacion(
                usuario_id=cerveza.usuario_id,
                actor_id=current_user.id,
                tipo="like",
                cerveza_id=cerveza_id
            ))
            db.commit()

    return resultado

@router.delete("/{cerveza_id}/me-gusta")
def unlike(
    cerveza_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return quitar_me_gusta(db, cerveza_id, current_user.id)