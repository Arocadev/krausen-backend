from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.core.security import hash_password, verify_password, create_access_token

def crear_usuario(db: Session, datos: UsuarioCreate) -> Usuario:
    if db.query(Usuario).filter(Usuario.email == datos.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese email"
        )
    if db.query(Usuario).filter(Usuario.username == datos.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese username"
        )
    usuario = Usuario(
        username=datos.username,
        email=datos.email,
        password_hash=hash_password(datos.password)
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def login_usuario(db: Session, email: str, password: str) -> dict:
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not verify_password(password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado"
        )
    token = create_access_token({"sub": usuario.email, "rol": usuario.rol.value, "id": usuario.id})
    return {"access_token": token, "token_type": "bearer"}