from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.valoracion import Valoracion
from app.schemas.valoracion import ValoracionCreate

def crear_valoracion(db: Session, cerveza_id: int, usuario_id: int, datos: ValoracionCreate) -> Valoracion:
    existente = db.query(Valoracion).filter(
        Valoracion.cerveza_id == cerveza_id,
        Valoracion.usuario_id == usuario_id
    ).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya has valorado esta cerveza"
        )
    valoracion = Valoracion(
        cerveza_id=cerveza_id,
        usuario_id=usuario_id,
        nota=datos.nota,
        comentario=datos.comentario
    )
    db.add(valoracion)
    db.commit()
    db.refresh(valoracion)
    return valoracion

def obtener_valoraciones(db: Session, cerveza_id: int):
    return db.query(Valoracion).filter(Valoracion.cerveza_id == cerveza_id).all()

def obtener_media(db: Session, cerveza_id: int) -> float:
    resultado = db.query(func.avg(Valoracion.nota)).filter(
        Valoracion.cerveza_id == cerveza_id
    ).scalar()
    return round(resultado, 1) if resultado else 0.0

def eliminar_valoracion(db: Session, valoracion_id: int, usuario_id: int):
    valoracion = db.query(Valoracion).filter(Valoracion.id == valoracion_id).first()
    if not valoracion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Valoración no encontrada"
        )
    if valoracion.usuario_id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes eliminar una valoración que no es tuya"
        )
    db.delete(valoracion)
    db.commit()