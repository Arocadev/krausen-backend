from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from app.models.base import get_db
from app.models.usuario import Usuario
from app.models.comentario import Comentario
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/cervezas", tags=["Comentarios"])

class ComentarioCreate(BaseModel):
    contenido: str

def comentario_a_dict(c: Comentario):
    return {
        "id": c.id,
        "contenido": c.contenido,
        "created_at": c.created_at.isoformat(),
        "usuario_id": c.usuario_id,
        "username": c.usuario.username if c.usuario else None,
    }

@router.get("/{cerveza_id}/comentarios")
def listar_comentarios(cerveza_id: int, db: Session = Depends(get_db)):
    comentarios = (
        db.query(Comentario)
        .options(joinedload(Comentario.usuario))
        .filter(Comentario.cerveza_id == cerveza_id)
        .order_by(Comentario.created_at.asc())
        .all()
    )
    return [comentario_a_dict(c) for c in comentarios]

@router.post("/{cerveza_id}/comentarios", status_code=201)
def crear_comentario(
    cerveza_id: int,
    datos: ComentarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if not datos.contenido.strip():
        raise HTTPException(status_code=400, detail="El comentario no puede estar vacío")
    comentario = Comentario(
        cerveza_id=cerveza_id,
        usuario_id=current_user.id,
        contenido=datos.contenido.strip()
    )
    db.add(comentario)
    db.commit()
    db.refresh(comentario)
    comentario = db.query(Comentario).options(joinedload(Comentario.usuario)).filter(Comentario.id == comentario.id).first()
    return comentario_a_dict(comentario)

@router.delete("/{cerveza_id}/comentarios/{comentario_id}", status_code=204)
def eliminar_comentario(
    cerveza_id: int,
    comentario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    comentario = db.query(Comentario).filter(
        Comentario.id == comentario_id,
        Comentario.cerveza_id == cerveza_id
    ).first()
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    if comentario.usuario_id != current_user.id and current_user.rol.value != "ADMIN":
        raise HTTPException(status_code=403, detail="No tienes permiso")
    db.delete(comentario)
    db.commit()