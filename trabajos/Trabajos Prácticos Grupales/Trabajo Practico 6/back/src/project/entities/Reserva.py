
from src.project.entities.Visitante import Visitante


class Reserva:
    def __init__(self, id: int, mail: str, visitantes: list[Visitante], fecha: str):
        self.id = id
        self.mail = mail
        self.visitantes = visitantes
        self.fecha = fecha