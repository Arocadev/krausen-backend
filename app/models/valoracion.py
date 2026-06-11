from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class MeGusta(Base):
    __tablename__ = "me_gustas"

    id = Column(Integer, primary_key=True, index=True)
    cerveza_id = Column(Integer, ForeignKey("cervezas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    cerveza = relationship("Cerveza", back_populates="me_gustas")
    usuario = relationship("Usuario")

    __table_args__ = (
        UniqueConstraint("cerveza_id", "usuario_id", name="uq_megusta_usuario_cerveza"),
    )