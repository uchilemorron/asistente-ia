from typing import Literal
from pydantic import BaseModel, Field

class Ticket(BaseModel):
    categoria: Literal["facturacion", "soporte_tecnico", "matricula", "otro"]
    urgencia: int = Field(ge=1, le=5)
    requiere_tecnico: bool
    resumen: str = Field(max_length=140)
