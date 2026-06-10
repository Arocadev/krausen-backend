from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.base import get_db
from app.models.ingrediente import Ingrediente
from app.schemas.cerveza import IngredienteBase
from app.services.ingrediente_service import obtener_ingredientes, crear_ingrediente, eliminar_ingrediente
from app.core.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/api/ingredientes", tags=["Ingredientes"])

@router.get("/", response_model=List[IngredienteBase])
def listar_ingredientes(db: Session = Depends(get_db)):
    return obtener_ingredientes(db)

@router.post("/", response_model=IngredienteBase, status_code=201)
def nuevo_ingrediente(
    nombre: str,
    tipo: str,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    return crear_ingrediente(db, nombre, tipo)

@router.delete("/{ingrediente_id}", status_code=204)
def borrar_ingrediente(
    ingrediente_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    eliminar_ingrediente(db, ingrediente_id)