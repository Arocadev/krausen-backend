from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.valoracion import MeGusta
from app.models.cerveza import Cerveza

def dar_me_gusta(db: Session, cerveza_id: int, usuario_id: int):
    cerveza = db.query(Cerveza).filter(Cerveza.id == cerveza_id).first()
    if not cerveza:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cerveza no encontrada")
    if cerveza.usuario_id == usuario_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes dar me gusta a tu propia cerveza")
    existente = db.query(MeGusta).filter(
        MeGusta.cerveza_id == cerveza_id,
        MeGusta.usuario_id == usuario_id
    ).first()
    if existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya has dado me gusta a esta cerveza")
    me_gusta = MeGusta(cerveza_id=cerveza_id, usuario_id=usuario_id)
    db.add(me_gusta)
    db.commit()
    return {"mensaje": "Me gusta añadido"}

def quitar_me_gusta(db: Session, cerveza_id: int, usuario_id: int):
    existente = db.query(MeGusta).filter(
        MeGusta.cerveza_id == cerveza_id,
        MeGusta.usuario_id == usuario_id
    ).first()
    if not existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No has dado me gusta a esta cerveza")
    db.delete(existente)
    db.commit()
    return {"mensaje": "Me gusta eliminado"}

def contar_me_gustas(db: Session, cerveza_id: int) -> int:
    return db.query(func.count(MeGusta.id)).filter(MeGusta.cerveza_id == cerveza_id).scalar()

def usuario_dio_me_gusta(db: Session, cerveza_id: int, usuario_id: int) -> bool:
    return db.query(MeGusta).filter(
        MeGusta.cerveza_id == cerveza_id,
        MeGusta.usuario_id == usuario_id
    ).first() is not None