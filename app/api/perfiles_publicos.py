from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.base import get_db
from app.models.usuario import Usuario
from app.models.cerveza import Cerveza
from app.models.valoracion import MeGusta

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

@router.get("/{username}")
def perfil_publico(username: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.username == username,
        Usuario.activo == 1
    ).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    recetas = (
        db.query(Cerveza)
        .options(joinedload(Cerveza.usuario))
        .filter(Cerveza.usuario_id == usuario.id, Cerveza.activa == True)
        .order_by(Cerveza.created_at.desc())
        .all()
    )

    me_gustas = (
        db.query(Cerveza)
        .options(joinedload(Cerveza.usuario))
        .join(MeGusta, Cerveza.id == MeGusta.cerveza_id)
        .filter(MeGusta.usuario_id == usuario.id, Cerveza.activa == True)
        .all()
    )

    total_likes_recibidos = sum(
        db.query(MeGusta).filter(MeGusta.cerveza_id == c.id).count()
        for c in recetas
    )

    def cerveza_dict(c):
        return {
            "id": c.id,
            "nombre": c.nombre,
            "descripcion": c.descripcion,
            "estilo": c.estilo,
            "alcohol": c.alcohol,
            "amargor": c.amargor,
            "parent_id": c.parent_id,
            "imagen_url": c.imagen_url,
            "username": c.usuario.username if c.usuario else None,
            "created_at": c.created_at.isoformat(),
        }

    return {
        "username": usuario.username,
        "created_at": usuario.created_at.isoformat(),
        "total_recetas": len(recetas),
        "total_likes_recibidos": total_likes_recibidos,
        "recetas": [cerveza_dict(c) for c in recetas],
        "me_gustas": [cerveza_dict(c) for c in me_gustas],
    }