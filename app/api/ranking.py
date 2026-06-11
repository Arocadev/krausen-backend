from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from app.models.base import get_db
from app.models.valoracion import MeGusta
from app.models.cerveza import Cerveza
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/ranking", tags=["Ranking"])

@router.get("/mensual")
def ranking_mensual(db: Session = Depends(get_db)):
    ahora = datetime.utcnow()

    resultado = (
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
        .filter(
            extract("month", MeGusta.created_at) == ahora.month,
            extract("year", MeGusta.created_at) == ahora.year
        )
        .group_by(Cerveza.id, Cerveza.nombre, Cerveza.estilo, Cerveza.usuario_id, Usuario.username)
        .order_by(func.count(MeGusta.id).desc())
        .limit(10)
        .all()
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
        for i, r in enumerate(resultado)
    ]