from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from app.models.base import get_db
from app.models.valoracion import Valoracion
from app.models.cerveza import Cerveza

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
            func.avg(Valoracion.nota).label("media"),
            func.count(Valoracion.id).label("total_valoraciones")
        )
        .join(Valoracion, Cerveza.id == Valoracion.cerveza_id)
        .filter(
            extract("month", Valoracion.created_at) == ahora.month,
            extract("year", Valoracion.created_at) == ahora.year
        )
        .group_by(Cerveza.id, Cerveza.nombre, Cerveza.estilo, Cerveza.usuario_id)
        .order_by(func.avg(Valoracion.nota).desc())
        .limit(10)
        .all()
    )

    return [
        {
            "posicion": i + 1,
            "id": r.id,
            "nombre": r.nombre,
            "estilo": r.estilo,
            "usuario_id": r.usuario_id,
            "media": round(float(r.media), 1),
            "total_valoraciones": r.total_valoraciones
        }
        for i, r in enumerate(resultado)
    ]