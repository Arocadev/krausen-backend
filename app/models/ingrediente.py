from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    tipo = Column(String(50), nullable=False)

    cervezas = relationship("CervezaIngrediente", back_populates="ingrediente")


class CervezaIngrediente(Base):
    __tablename__ = "cerveza_ingredientes"

    id = Column(Integer, primary_key=True, index=True)
    cerveza_id = Column(Integer, ForeignKey("cervezas.id"), nullable=False)
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"), nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad = Column(String(20), nullable=False)

    cerveza = relationship("Cerveza", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente", back_populates="cervezas")