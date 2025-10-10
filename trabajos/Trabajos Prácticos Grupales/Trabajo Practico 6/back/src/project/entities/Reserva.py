
from src.project.entities.Visitante import Visitante


class Reserva:
    def __init__(self, mail: str, visitantes: list[Visitante], fecha: str):
        self.mail = mail
        self.visitantes = visitantes
        self.fecha = fecha