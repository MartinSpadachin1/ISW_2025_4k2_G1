from typing import Optional
from sqlmodel import Field, SQLModel
from src.common.entradas import VIP, GENERAL, PRECIO_GENERAL, PRECIO_VIP



class VisitanteBase(SQLModel):
    edad: int
    tipo_entrada: str

class Visitante(VisitanteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monto_final: float

    def calcular_monto(edad: int, tipo_entrada: str) -> float:

        if not(0 <= edad <= 120):
            raise ValueError("La edad debe estar entre 0 y 120 años.")
        
        if tipo_entrada == VIP:
            precio = PRECIO_VIP
        elif tipo_entrada == GENERAL:
            precio = PRECIO_GENERAL
        else:
            raise ValueError("Tipo de entrada no válido.")
        
        if edad <= 3:
            return 0.0
        elif (edad < 15 or edad >= 60):
            precio *= 0.5

        return round(precio, 2)