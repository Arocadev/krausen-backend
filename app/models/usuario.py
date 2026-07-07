from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.models import notificacion
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy.orm import relationship
import enum

class Rol(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    rol = Column(Enum(Rol), default=Rol.USER, nullable=False)
    activo = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    reset_token = Column(String(100), nullable=True)
    reset_token_expira = Column(DateTime, nullable=True)

    cervezas = relationship("Cerveza", back_populates="usuario")
    notificaciones = relationship("Notificacion", foreign_keys="Notificacion.usuario_id", back_populates="usuario")