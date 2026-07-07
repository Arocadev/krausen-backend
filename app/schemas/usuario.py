from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from app.models.usuario import Rol
import re


class UsuarioCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def validar_username(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError("El username debe tener al menos 3 caracteres")
        if len(v) > 50:
            raise ValueError("El username no puede superar 50 caracteres")
        if not re.match(r"^[a-zA-Z0-9_\-]+$", v):
            raise ValueError("El username solo puede contener letras, números, guiones y guiones bajos")
        return v

    @field_validator("password")
    @classmethod
    def validar_password(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if len(v) > 100:
            raise ValueError("La contraseña no puede superar 100 caracteres")
        return v


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


class SolicitarRecuperacion(BaseModel):
    email: EmailStr


class ResetearPassword(BaseModel):
    token: str
    password_nueva: str

    @field_validator("token")
    @classmethod
    def validar_token(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El token no puede estar vacío")
        if len(v) > 200:
            raise ValueError("Token inválido")
        return v

    @field_validator("password_nueva")
    @classmethod
    def validar_password_nueva(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if len(v) > 100:
            raise ValueError("La contraseña no puede superar 100 caracteres")
        return v