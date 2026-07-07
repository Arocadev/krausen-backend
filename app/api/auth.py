from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, Token, UsuarioLogin, SolicitarRecuperacion, ResetearPassword
from app.services.usuario_service import crear_usuario, login_usuario
from app.core.security import hash_password
import os
import resend
import secrets
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/registro", response_model=UsuarioResponse, status_code=201)
def registro(datos: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, datos)

@router.post("/login", response_model=Token)
def login(datos: UsuarioLogin, db: Session = Depends(get_db)):
    return login_usuario(db, datos.email, datos.password)

@router.post("/solicitar-recuperacion")
def solicitar_recuperacion(datos: SolicitarRecuperacion, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == datos.email).first()
    if not usuario:
        return {"mensaje": "Si el email existe, recibirás un correo con instrucciones."}

    token = secrets.token_urlsafe(32)
    usuario.reset_token = token
    usuario.reset_token_expira = datetime.utcnow() + timedelta(hours=1)
    db.commit()

    try:
        resend.api_key = os.getenv("RESEND_API_KEY")
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": [usuario.email],
            "subject": "Recuperación de contraseña — Krausen",
            "html": f"""
                <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto;">
                    <h2 style="color: #33220F;">Recupera tu contraseña</h2>
                    <p style="color: #5C3A21;">Haz clic en el siguiente botón para restablecer tu contraseña. El enlace expira en 1 hora.</p>
                    <a href="http://localhost:3000/reset-password?token={token}"
                       style="display: inline-block; background: #C8861B; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: 600; margin: 16px 0;">
                        Restablecer contraseña
                    </a>
                    <p style="color: #5C3A21; font-size: 13px;">Si no solicitaste este cambio, ignora este email.</p>
                </div>
            """
        })
    except Exception as e:
        print(f"Error enviando email: {e}")

    return {"mensaje": "Si el email existe, recibirás un correo con instrucciones."}

@router.post("/reset-password")
def reset_password(datos: ResetearPassword, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.reset_token == datos.token,
    ).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")

    if usuario.reset_token_expira < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token inválido o expirado")

    usuario.password_hash = hash_password(datos.password_nueva)
    usuario.reset_token = None
    usuario.reset_token_expira = None
    db.commit()

    return {"mensaje": "Contraseña actualizada correctamente"}