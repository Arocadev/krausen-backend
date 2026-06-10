from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, Token, UsuarioLogin
from app.services.usuario_service import crear_usuario, login_usuario

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/registro", response_model=UsuarioResponse, status_code=201)
def registro(datos: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, datos)

@router.post("/login", response_model=Token)
def login(datos: UsuarioLogin, db: Session = Depends(get_db)):
    return login_usuario(db, datos.email, datos.password)