from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.base import get_db
from app.models.usuario import Usuario
from app.models.cerveza import Cerveza
from app.schemas.cerveza import CervezaCreate, CervezaResponse
from app.services.cerveza_service import crear_cerveza, obtener_cervezas, obtener_cerveza, eliminar_cerveza
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/cervezas", tags=["Cervezas"])

@router.get("/", response_model=List[CervezaResponse])
def listar_cervezas(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return obtener_cervezas(db, skip, limit)

@router.get("/mis-recetas", response_model=List[CervezaResponse])
def mis_recetas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Cerveza).filter(Cerveza.usuario_id == current_user.id).all()

@router.get("/{cerveza_id}", response_model=CervezaResponse)
def detalle_cerveza(cerveza_id: int, db: Session = Depends(get_db)):
    return obtener_cerveza(db, cerveza_id)

@router.post("/", response_model=CervezaResponse, status_code=201)
def nueva_cerveza(
    datos: CervezaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return crear_cerveza(db, datos, current_user.id)

@router.post("/{cerveza_id}/fork", response_model=CervezaResponse, status_code=201)
def fork_cerveza(
    cerveza_id: int,
    datos: CervezaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    datos.parent_id = cerveza_id
    return crear_cerveza(db, datos, current_user.id)

@router.delete("/{cerveza_id}", status_code=204)
def borrar_cerveza(
    cerveza_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    eliminar_cerveza(db, cerveza_id, current_user.id)