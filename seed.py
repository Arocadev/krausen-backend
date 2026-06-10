from app.models.base import SessionLocal
from app.core.seed import seed_ingredientes

db = SessionLocal()
try:
    seed_ingredientes(db)
finally:
    db.close()