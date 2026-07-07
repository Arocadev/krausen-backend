from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime
from typing import Optional, List


class PasoBase(BaseModel):
    orden: int
    descripcion: str
    duracion_min: Optional[int] = None

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("La descripción del paso no puede estar vacía")
        if len(v) > 1000:
            raise ValueError("La descripción del paso no puede superar 1000 caracteres")
        return v

    @field_validator("duracion_min")
    @classmethod
    def validar_duracion(cls, v):
        if v is not None and v < 0:
            raise ValueError("La duración no puede ser negativa")
        if v is not None and v > 10080:
            raise ValueError("La duración no puede superar 7 días (10080 minutos)")
        return v


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

    @field_validator("cantidad")
    @classmethod
    def validar_cantidad(cls, v):
        if v <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        if v > 100000:
            raise ValueError("La cantidad parece excesiva (máx. 100000)")
        return v

    @field_validator("unidad")
    @classmethod
    def validar_unidad(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("La unidad no puede estar vacía")
        if len(v) > 20:
            raise ValueError("La unidad no puede superar 20 caracteres")
        return v


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
    dias_fermentacion: Optional[int] = None
    intervalo_horas: Optional[int] = None

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío")
        if len(v) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        if len(v) > 100:
            raise ValueError("El nombre no puede superar 100 caracteres")
        return v

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) > 2000:
                raise ValueError("La descripción no puede superar 2000 caracteres")
        return v

    @field_validator("estilo")
    @classmethod
    def validar_estilo(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) > 100:
                raise ValueError("El estilo no puede superar 100 caracteres")
        return v

    @field_validator("litros")
    @classmethod
    def validar_litros(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError("Los litros deben ser mayor que 0")
            if v > 10000:
                raise ValueError("Los litros no pueden superar 10000")
        return v

    @field_validator("alcohol")
    @classmethod
    def validar_alcohol(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("El alcohol no puede ser negativo")
            if v > 100:
                raise ValueError("El alcohol no puede superar 100%")
        return v

    @field_validator("amargor")
    @classmethod
    def validar_amargor(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("El amargor (IBU) no puede ser negativo")
            if v > 1000:
                raise ValueError("El amargor (IBU) no puede superar 1000")
        return v

    @field_validator("dias_fermentacion")
    @classmethod
    def validar_dias_fermentacion(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Los días de fermentación no pueden ser negativos")
            if v > 365:
                raise ValueError("Los días de fermentación no pueden superar 365")
        return v

    @field_validator("intervalo_horas")
    @classmethod
    def validar_intervalo_horas(cls, v):
        if v is not None:
            if v < 1:
                raise ValueError("El intervalo mínimo es 1 hora")
            if v > 168:
                raise ValueError("El intervalo no puede superar 168 horas (1 semana)")
        return v

    @model_validator(mode="after")
    def validar_pasos_ordenados(self):
        if self.pasos:
            ordenes = [p.orden for p in self.pasos]
            if len(ordenes) != len(set(ordenes)):
                raise ValueError("Los pasos no pueden tener órdenes duplicados")
        return self


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
    activa: bool
    imagen_url: Optional[str]
    ingredientes: List[CervezaIngredienteResponse] = []
    pasos: List[PasoResponse] = []

    class Config:
        from_attributes = True