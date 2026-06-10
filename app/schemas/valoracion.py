from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ValoracionCreate(BaseModel):
    nota: int = Field(..., ge=0, le=10)
    comentario: Optional[str] = None

class ValoracionResponse(BaseModel):
    id: int
    cerveza_id: int
    usuario_id: int
    nota: int
    comentario: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True