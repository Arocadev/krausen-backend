from app.models.base import SessionLocal
from app.models.usuario import Usuario, Rol
from app.core.security import hash_password

db = SessionLocal()

admin = Usuario(
    username="admin",
    email="admin@krausen.beer",
    password_hash=hash_password("admin1234"),
    rol=Rol.ADMIN
)

user = Usuario(
    username="cervecero",
    email="cervecero@krausen.beer",
    password_hash=hash_password("cervecero1234"),
    rol=Rol.USER
)

db.add(admin)
db.add(user)
db.commit()
print("✅ Usuarios creados:")
print("  Admin: admin@krausen.beer / admin1234")
print("  User: cervecero@krausen.beer / cervecero1234")
db.close()