
from src.project.entities.Visitante import Visitante


class Reserva:
    def __init__(self, id:int, mail: str, visitantes: list[Visitante], fecha: str, tipo_pago: str):
        self.id = id
        self.mail = mail
        self.visitantes = visitantes
        self.fecha = fecha
        self.tipo_pago = tipo_pago
        self.pago_realizado = False


    def total_monto(self) -> float:
        return sum(visitante.monto for visitante in self.visitantes)