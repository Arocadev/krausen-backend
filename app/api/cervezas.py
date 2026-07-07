from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
import uuid, os, shutil
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

@router.post("/{cerveza_id}/imagen", status_code=200)
async def subir_imagen(
    cerveza_id: int,
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    cerveza = db.query(Cerveza).filter(Cerveza.id == cerveza_id).first()
    if not cerveza:
        raise HTTPException(status_code=404, detail="Cerveza no encontrada")
    if cerveza.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso")

    extension = imagen.filename.split(".")[-1].lower()
    if extension not in ["jpg", "jpeg", "png", "webp"]:
        raise HTTPException(status_code=400, detail="Formato no permitido. Usa JPG, PNG o WebP.")

    nombre_archivo = f"{uuid.uuid4()}.{extension}"
    ruta = f"uploads/cervezas/{nombre_archivo}"

    with open(ruta, "wb") as f:
        shutil.copyfileobj(imagen.file, f)

    if cerveza.imagen_url:
        ruta_anterior = cerveza.imagen_url.lstrip("/")
        if os.path.exists(ruta_anterior):
            os.remove(ruta_anterior)

    cerveza.imagen_url = f"/uploads/cervezas/{nombre_archivo}"
    db.commit()
    return {"imagen_url": cerveza.imagen_url}

@router.get("/")
def listar_cervezas(skip: int = 0, limit: int = 12, db: Session = Depends(get_db)):
    total = db.query(Cerveza).filter(Cerveza.activa == True).count()
    cervezas = (
        db.query(Cerveza)
        .options(joinedload(Cerveza.usuario))
        .filter(Cerveza.activa == True)
        .order_by(Cerveza.created_at.desc())
        .offset(skip).limit(limit).all()
    )
    return {"total": total, "cervezas": [cerveza_con_username(c) for c in cervezas]}

@router.get("/buscar")
def buscar_cervezas(
    q: str = "",
    estilo: str = "",
    alcohol_min: float = 0,
    alcohol_max: float = 100,
    amargor_min: int = 0,
    amargor_max: int = 200,
    ingrediente: str = "",
    autor: str = "",
    skip: int = 0,
    limit: int = 12,
    db: Session = Depends(get_db)
):
    query = db.query(Cerveza).options(joinedload(Cerveza.usuario)).filter(Cerveza.activa == True)

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
    if ingrediente:
        from app.models.ingrediente import Ingrediente, CervezaIngrediente
        query = query.join(CervezaIngrediente, Cerveza.id == CervezaIngrediente.cerveza_id)\
                     .join(Ingrediente, CervezaIngrediente.ingrediente_id == Ingrediente.id)\
                     .filter(Ingrediente.nombre.ilike(f"%{ingrediente}%"))
    if autor:
        query = query.join(Usuario, Cerveza.usuario_id == Usuario.id)\
                     .filter(Usuario.username.ilike(f"%{autor}%"))

    total = query.count()
    cervezas = query.order_by(Cerveza.created_at.desc()).offset(skip).limit(limit).all()
    return {"total": total, "cervezas": [cerveza_con_username(c) for c in cervezas]}

@router.get("/tiene-forks/{cerveza_id}")
def tiene_forks(cerveza_id: int, db: Session = Depends(get_db)):
    total = db.query(Cerveza).filter(Cerveza.parent_id == cerveza_id).count()
    return {"tiene_forks": total > 0, "total_forks": total}

@router.get("/arbol/{cerveza_id}")
def arbol_forks(cerveza_id: int, db: Session = Depends(get_db)):
    cerveza = db.query(Cerveza).filter(Cerveza.id == cerveza_id).first()
    if not cerveza:
        raise HTTPException(status_code=404, detail="Cerveza no encontrada")

    # Encontrar la raíz subiendo por parent_id
    raiz_id = cerveza_id
    actual = cerveza
    visitados = set()
    while actual.parent_id and actual.parent_id not in visitados:
        visitados.add(actual.id)
        padre = db.query(Cerveza).filter(Cerveza.id == actual.parent_id).first()
        if not padre:
            break
        actual = padre
        raiz_id = actual.id

    # CTE recursiva: una sola query para todo el árbol
    cte_sql = text("""
        WITH RECURSIVE arbol AS (
            SELECT id, nombre, usuario_id, parent_id
            FROM cervezas
            WHERE id = :raiz_id
            UNION ALL
            SELECT c.id, c.nombre, c.usuario_id, c.parent_id
            FROM cervezas c
            INNER JOIN arbol a ON c.parent_id = a.id
        )
        SELECT arbol.id, arbol.nombre, arbol.parent_id, u.username
        FROM arbol
        JOIN usuarios u ON arbol.usuario_id = u.id
    """)

    filas = db.execute(cte_sql, {"raiz_id": raiz_id}).fetchall()
    mapa = {
        f.id: {
            "id": f.id,
            "nombre": f.nombre,
            "parent_id": f.parent_id,
            "username": f.username,
            "es_actual": f.id == cerveza_id,
            "hijos": []
        }
        for f in filas
    }

    raiz = None
    for nodo in mapa.values():
        if nodo["parent_id"] in mapa:
            mapa[nodo["parent_id"]]["hijos"].append(nodo)
        else:
            raiz = nodo

    return raiz if raiz else mapa.get(raiz_id)

@router.get("/mis-recetas")
def mis_recetas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    cervezas = (
        db.query(Cerveza)
        .options(joinedload(Cerveza.usuario))
        .filter(Cerveza.usuario_id == current_user.id)
        .order_by(Cerveza.created_at.desc())
        .all()
    )
    return [cerveza_con_username(c) for c in cervezas]

@router.get("/me-gustan")
def recetas_que_me_gustan(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    from app.models.valoracion import MeGusta
    cervezas = (
        db.query(Cerveza)
        .options(joinedload(Cerveza.usuario))
        .join(MeGusta, Cerveza.id == MeGusta.cerveza_id)
        .filter(MeGusta.usuario_id == current_user.id)
        .all()
    )
    return [cerveza_con_username(c) for c in cervezas]

@router.patch("/{cerveza_id}/activacion")
def toggle_activacion(
    cerveza_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    cerveza = db.query(Cerveza).filter(Cerveza.id == cerveza_id).first()
    if not cerveza:
        raise HTTPException(status_code=404, detail="Cerveza no encontrada")
    if cerveza.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso")
    cerveza.activa = not cerveza.activa
    db.commit()
    return {"activa": cerveza.activa}

@router.get("/{cerveza_id}")
def detalle_cerveza(cerveza_id: int, db: Session = Depends(get_db)):
    cerveza = db.query(Cerveza).options(
        joinedload(Cerveza.usuario),
        joinedload(Cerveza.ingredientes),
        joinedload(Cerveza.pasos)
    ).filter(Cerveza.id == cerveza_id).first()
    if not cerveza:
        raise HTTPException(status_code=404, detail="Cerveza no encontrada")
    return cerveza_con_username(cerveza)

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
    from app.models.notificacion import Notificacion

    datos.parent_id = cerveza_id
    cerveza = crear_cerveza(db, datos, current_user.id)
    cerveza = db.query(Cerveza).options(joinedload(Cerveza.usuario)).filter(Cerveza.id == cerveza.id).first()

    original = db.query(Cerveza).filter(Cerveza.id == cerveza_id).first()
    if original and original.usuario_id != current_user.id:
        db.add(Notificacion(
            usuario_id=original.usuario_id,
            actor_id=current_user.id,
            tipo="fork",
            cerveza_id=cerveza_id
        ))
        db.commit()

    return cerveza_con_username(cerveza)

@router.delete("/{cerveza_id}", status_code=204)
def borrar_cerveza(
    cerveza_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    eliminar_cerveza(db, cerveza_id, current_user.id)