from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class RegistroTemperatura(Base):
    __tablename__ = "registros_temperatura"

    id = Column(Integer, primary_key=True, index=True)
    cerveza_id = Column(Integer, ForeignKey("cervezas.id"), nullable=False)
    slot = Column(Integer, nullable=False)
    temperatura = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    cerveza = relationship("Cerveza", back_populates="temperaturas")