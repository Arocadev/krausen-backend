from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.models.base import get_db
from app.models.usuario import Usuario
from app.models.cerveza import Cerveza
from app.schemas.cerveza import CervezaCreate, CervezaResponse
from app.services.cerveza_service import crear_cerveza, obtener_cervezas, obtener_cerveza, eliminar_cerveza
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/cervezas", tags=["Cervezas"])

def cerveza_con_username(cerveza):
    data = CervezaResponse.model_validate(cerveza).model_dump()
    data["username"] = cerveza.usuario.username if cerveza.usuario else None
    return data

@router.get("/")
def listar_cervezas(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    cervezas = db.query(Cerveza).options(joinedload(Cerveza.usuario)).offset(skip).limit(limit).all()
    return [cerveza_con_username(c) for c in cervezas]

@router.get("/buscar")
def buscar_cervezas(
    q: str = "",
    estilo: str = "",
    alcohol_min: float = 0,
    alcohol_max: float = 100,
    amargor_min: int = 0,
    amargor_max: int = 200,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Cerveza).options(joinedload(Cerveza.usuario))

    if q:
        query = query.filter(Cerveza.nombre.ilike(f"%{q}%"))
    if estilo:
        query = query.filter(Cerveza.estilo.ilike(f"%{estilo}%"))
    if alcohol_min > 0:
        query = query.filter(Cerveza.alcohol >= alcohol_min)
    if alcohol_max < 100:
        query = query.filter(Cerveza.alcohol <= alcohol_max)
    if amargor_min > 0:
        query = query.filter(Cerveza.amargor >= amargor_min)
    if amargor_max < 200:
        query = query.filter(Cerveza.amargor <= amargor_max)

    cervezas = query.order_by(Cerveza.created_at.desc()).offset(skip).limit(limit).all()
    return [cerveza_con_username(c) for c in cervezas]

@router.get("/tiene-forks/{cerveza_id}")
def tiene_forks(cerveza_id: int, db: Session = Depends(get_db)):
    total = db.query(Cerveza).filter(Cerveza.parent_id == cerveza_id).count()
    return {"tiene_forks": total > 0, "total_forks": total}

@router.put("/{cerveza_id}")
def editar_cerveza_endpoint(
    cerveza_id: int,
    datos: CervezaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    from app.services.cerveza_service import editar_cerveza
    cerveza = editar_cerveza(db, cerveza_id, datos, current_user.id)
    cerveza = db.query(Cerveza).options(joinedload(Cerveza.usuario)).filter(Cerveza.id == cerveza.id).first()
    return cerveza_con_username(cerveza)

@router.get("/mis-recetas")
def mis_recetas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    cervezas = db.query(Cerveza).options(joinedload(Cerveza.usuario)).filter(Cerveza.usuario_id == current_user.id).all()
    return [cerveza_con_username(c) for c in cervezas]

@router.get("/{cerveza_id}")
def detalle_cerveza(cerveza_id: int, db: Session = Depends(get_db)):
    cerveza = db.query(Cerveza).options(
        joinedload(Cerveza.usuario),
        joinedload(Cerveza.ingredientes),
        joinedload(Cerveza.pasos)
    ).filter(Cerveza.id == cerveza_id).first()
    if not cerveza:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cerveza no encontrada")
    return cerveza_con_username(cerveza)

@router.post("/", status_code=201)
def nueva_cerveza(
    datos: CervezaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    cerveza = crear_cerveza(db, datos, current_user.id)
    cerveza = db.query(Cerveza).options(joinedload(Cerveza.usuario)).filter(Cerveza.id == cerveza.id).first()
    return cerveza_con_username(cerveza)

@router.post("/{cerveza_id}/fork", status_code=201)
def fork_cerveza(
    cerveza_id: int,
    datos: CervezaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    datos.parent_id = cerveza_id
    cerveza = crear_cerveza(db, datos, current_user.id)
    cerveza = db.query(Cerveza).options(joinedload(Cerveza.usuario)).filter(Cerveza.id == cerveza.id).first()
    return cerveza_con_username(cerveza)

@router.delete("/{cerveza_id}", status_code=204)
def borrar_cerveza(
    cerveza_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    eliminar_cerveza(db, cerveza_id, current_user.id)