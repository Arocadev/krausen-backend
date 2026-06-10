from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.usuario import Rol

class UsuarioCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: str
    rol: Rol
    activo: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None