from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.cerveza import Cerveza
from app.models.ingrediente import CervezaIngrediente
from app.models.paso import Paso
from app.schemas.cerveza import CervezaCreate

def crear_cerveza(db: Session, datos: CervezaCreate, usuario_id: int) -> Cerveza:
    if datos.parent_id:
        parent = db.query(Cerveza).filter(Cerveza.id == datos.parent_id).first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La cerveza original no existe"
            )
    cerveza = Cerveza(
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        estilo=datos.estilo,
        litros=datos.litros,
        alcohol=datos.alcohol,
        amargor=datos.amargor,
        parent_id=datos.parent_id,
        usuario_id=usuario_id
    )
    db.add(cerveza)
    db.flush()

    for ing in datos.ingredientes:
        ci = CervezaIngrediente(
            cerveza_id=cerveza.id,
            ingrediente_id=ing.ingrediente_id,
            cantidad=ing.cantidad,
            unidad=ing.unidad
        )
        db.add(ci)

    for i, paso in enumerate(datos.pasos):
        p = Paso(
            cerveza_id=cerveza.id,
            orden=i + 1,
            descripcion=paso.descripcion,
            duracion_min=paso.duracion_min
        )
        db.add(p)

    db.commit()
    db.refresh(cerveza)
    return cerveza

def obtener_cervezas(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Cerveza).offset(skip).limit(limit).all()

def obtener_cerveza(db: Session, cerveza_id: int) -> Cerveza:
    cerveza = db.query(Cerveza).filter(Cerveza.id == cerveza_id).first()
    if not cerveza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cerveza no encontrada"
        )
    return cerveza

def eliminar_cerveza(db: Session, cerveza_id: int, usuario_id: int):
    cerveza = obtener_cerveza(db, cerveza_id)
    if cerveza.usuario_id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes eliminar una cerveza que no es tuya"
        )
    db.delete(cerveza)
    db.commit()