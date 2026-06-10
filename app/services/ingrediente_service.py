from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.ingrediente import Ingrediente

def obtener_ingredientes(db: Session):
    return db.query(Ingrediente).all()

def obtener_ingrediente(db: Session, ingrediente_id: int) -> Ingrediente:
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if not ingrediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente no encontrado"
        )
    return ingrediente

def crear_ingrediente(db: Session, nombre: str, tipo: str) -> Ingrediente:
    existente = db.query(Ingrediente).filter(Ingrediente.nombre == nombre).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un ingrediente con ese nombre"
        )
    ingrediente = Ingrediente(nombre=nombre, tipo=tipo)
    db.add(ingrediente)
    db.commit()
    db.refresh(ingrediente)
    return ingrediente

def eliminar_ingrediente(db: Session, ingrediente_id: int):
    ingrediente = obtener_ingrediente(db, ingrediente_id)
    db.delete(ingrediente)
    db.commit()