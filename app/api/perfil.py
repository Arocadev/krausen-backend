from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.base import get_db
from app.models.usuario import Usuario
from app.core.deps import get_current_user
from app.core.security import verify_password, hash_password

router = APIRouter(prefix="/api/perfil", tags=["Perfil"])

class CambiarPassword(BaseModel):
    password_actual: str
    password_nueva: str
    password_confirmar: str

class PerfilResponse(BaseModel):
    id: int
    username: str
    email: str
    rol: str
    created_at: str

    class Config:
        from_attributes = True

@router.get("/", response_model=PerfilResponse)
def obtener_perfil(current_user: Usuario = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "rol": current_user.rol.value,
        "created_at": str(current_user.created_at),
    }

@router.put("/password")
def cambiar_password(
    datos: CambiarPassword,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if not verify_password(datos.password_actual, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña actual es incorrecta"
        )
    if datos.password_nueva != datos.password_confirmar:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las contraseñas nuevas no coinciden"
        )
    if len(datos.password_nueva) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La nueva contraseña debe tener al menos 8 caracteres"
        )
    current_user.password_hash = hash_password(datos.password_nueva)
    db.commit()
    return {"mensaje": "Contraseña actualizada correctamente"}