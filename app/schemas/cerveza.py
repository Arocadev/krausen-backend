from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class PasoBase(BaseModel):
    orden: int
    descripcion: str
    duracion_min: Optional[int] = None

class PasoResponse(PasoBase):
    id: int
    class Config:
        from_attributes = True

class IngredienteBase(BaseModel):
    id: int
    nombre: str
    tipo: str
    class Config:
        from_attributes = True

class CervezaIngredienteBase(BaseModel):
    ingrediente_id: int
    cantidad: float
    unidad: str

class CervezaIngredienteResponse(BaseModel):
    ingrediente: IngredienteBase
    cantidad: float
    unidad: str
    class Config:
        from_attributes = True

class CervezaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estilo: Optional[str] = None
    litros: Optional[int] = None
    alcohol: Optional[float] = None
    amargor: Optional[int] = None
    parent_id: Optional[int] = None
    ingredientes: List[CervezaIngredienteBase] = []
    pasos: List[PasoBase] = []

class CervezaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    estilo: Optional[str]
    litros: Optional[int]
    alcohol: Optional[float]
    amargor: Optional[int]
    parent_id: Optional[int]
    usuario_id: int
    created_at: datetime
    ingredientes: List[CervezaIngredienteResponse] = []
    pasos: List[PasoResponse] = []

    class Config:
        from_attributes = True