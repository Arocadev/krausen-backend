from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class Valoracion(Base):
    __tablename__ = "valoraciones"

    id = Column(Integer, primary_key=True, index=True)
    cerveza_id = Column(Integer, ForeignKey("cervezas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nota = Column(Integer, nullable=False)
    comentario = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    cerveza = relationship("Cerveza", back_populates="valoraciones")
    usuario = relationship("Usuario")

    __table_args__ = (
        UniqueConstraint("cerveza_id", "usuario_id", name="uq_valoracion_usuario_cerveza"),
    )