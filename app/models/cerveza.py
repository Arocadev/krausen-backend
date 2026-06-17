from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class Cerveza(Base):
    __tablename__ = "cervezas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("cervezas.id"), nullable=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    estilo = Column(String(50), nullable=True)
    litros = Column(Integer, nullable=True)
    alcohol = Column(Float, nullable=True)
    amargor = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    dias_fermentacion = Column(Integer, nullable=True)
    intervalo_horas = Column(Integer, nullable=True)

    usuario = relationship("Usuario", back_populates="cervezas")
    parent = relationship("Cerveza", remote_side=[id])
    ingredientes = relationship("CervezaIngrediente", back_populates="cerveza")
    pasos = relationship("Paso", back_populates="cerveza", order_by="Paso.orden")
    me_gustas = relationship("MeGusta", back_populates="cerveza")
    temperaturas = relationship("RegistroTemperatura", back_populates="cerveza", order_by="RegistroTemperatura.slot")