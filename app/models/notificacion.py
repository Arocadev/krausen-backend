from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    actor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(String(20), nullable=False)  # "like" | "fork"
    cerveza_id = Column(Integer, ForeignKey("cervezas.id"), nullable=False)
    leida = Column(Boolean, default=False, nullable=False, server_default="false")
    created_at = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    actor = relationship("Usuario", foreign_keys=[actor_id])
    cerveza = relationship("Cerveza")