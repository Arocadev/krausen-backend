from app.models.base import SessionLocal
from app.models.usuario import Usuario, Rol
from app.core.security import hash_password

db = SessionLocal()

usuarios = [
    {"username": "demo", "email": "demo@krausen.beer", "rol": Rol.USER},
    {"username": "carlos", "email": "carlos@krausen.beer", "rol": Rol.USER},
    {"username": "sara", "email": "sara@krausen.beer", "rol": Rol.USER},
    {"username": "miguel", "email": "miguel@krausen.beer", "rol": Rol.USER},
]

for u in usuarios:
    existe = db.query(Usuario).filter(Usuario.username == u["username"]).first()
    if not existe:
        db.add(Usuario(
            username=u["username"],
            email=u["email"],
            password_hash=hash_password("krausen1234"),
            rol=u["rol"],
            activo=1
        ))

db.commit()
db.close()
print("Usuarios creados.")