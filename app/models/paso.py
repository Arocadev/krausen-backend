from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Paso(Base):
    __tablename__ = "pasos"

    id = Column(Integer, primary_key=True, index=True)
    cerveza_id = Column(Integer, ForeignKey("cervezas.id"), nullable=False)
    orden = Column(Integer, nullable=False)
    descripcion = Column(String(500), nullable=False)
    duracion_min = Column(Integer, nullable=True)

    cerveza = relationship("Cerveza", back_populates="pasos")