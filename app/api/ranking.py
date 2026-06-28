from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from app.models.base import get_db
from app.models.valoracion import MeGusta
from app.models.cerveza import Cerveza
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/ranking", tags=["Ranking"])

def _query_ranking(db, filtro=None, limit=10):
    q = (
        db.query(
            Cerveza.id,
            Cerveza.nombre,
            Cerveza.estilo,
            Cerveza.usuario_id,
            Usuario.username,
            func.count(MeGusta.id).label("total_likes")
        )
        .join(MeGusta, Cerveza.id == MeGusta.cerveza_id)
        .join(Usuario, Cerveza.usuario_id == Usuario.id)
    )
    if filtro is not None:
        q = q.filter(filtro)
    q = (
        q.group_by(Cerveza.id, Cerveza.nombre, Cerveza.estilo, Cerveza.usuario_id, Usuario.username)
        .order_by(func.count(MeGusta.id).desc())
        .limit(limit)
    )
    return [
        {
            "posicion": i + 1,
            "id": r.id,
            "nombre": r.nombre,
            "estilo": r.estilo,
            "username": r.username,
            "total_likes": r.total_likes
        }
        for i, r in enumerate(q.all())
    ]

@router.get("/mensual")
def ranking_mensual(db: Session = Depends(get_db)):
    ahora = datetime.utcnow()
    filtro = (
        extract("month", MeGusta.created_at) == ahora.month,
        extract("year", MeGusta.created_at) == ahora.year
    )
    from sqlalchemy import and_
    return _query_ranking(db, and_(*filtro))

@router.get("/anual")
def ranking_anual(db: Session = Depends(get_db)):
    ahora = datetime.utcnow()
    from sqlalchemy import and_
    return _query_ranking(db, extract("year", MeGusta.created_at) == ahora.year)

@router.get("/global")
def ranking_global(db: Session = Depends(get_db)):
    return _query_ranking(db)