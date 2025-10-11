from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, Session
from src.common.entradas import VIP, GENERAL, PRECIO_GENERAL, PRECIO_VIP



#Modelo Visitante
class Visitante(SQLModel, table=True):
    __tablename__ = "visitantes"
    id: Optional[int] = Field(default=None, primary_key=True)
    edad: int
    tipo_entrada: str
    monto_final: float

    #Clave foranea a la tabla reservas
    reserva_id: Optional[int] = Field(default=None, foreign_key="reservas.id")
    reserva: Optional["Reserva"] = Relationship(back_populates="visitantes")


#Modelo Reserva
class Reserva(SQLModel, table=True):
    __tablename__ = "reservas"
    id: Optional[int] = Field(default=None, primary_key=True)
    mail: str
    fecha: str
    visitantes: list[Visitante] = Relationship(back_populates="reserva")
    tipo_pago: str
    pago_realizado: bool = Field(default=False)

    def total_monto(self) -> float:
        return sum(visitante.monto_final for visitante in self.visitantes)


#Modelo Usuario
class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=1, max_length=50)
    email: str
    hashed_password: str
    is_active: bool = Field(default=True)
