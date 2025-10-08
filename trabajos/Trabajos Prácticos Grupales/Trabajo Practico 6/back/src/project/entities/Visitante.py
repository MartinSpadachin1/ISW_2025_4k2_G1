from src.common.entradas import VIP, GENERAL, PRECIO_GENERAL, PRECIO_VIP


class Visitante: 
    """Clase que representa a un visitante con su edad, tipo de entrada y monto a pagar."""
    def __init__(self, edad: int, tipo_entrada: str):
        """Inicializa un visitante con su edad, tipo de entrada y calcula el monto a pagar."""
        self.edad = edad
        self.tipo_entrada = tipo_entrada
        self.monto = self.calcular_monto(edad, tipo_entrada)

    def calcular_monto(self, edad: int, tipo_entrada: str) -> float:
        """Calcula el monto a pagar según la edad y el tipo de entrada."""
        if tipo_entrada == VIP:
            precio = PRECIO_VIP  # Precio base para entrada VIP
        elif tipo_entrada == GENERAL:
            precio = PRECIO_GENERAL  # Precio base para entrada GENERAL

        if (edad < 15 or edad >= 60) and edad > 3:
            precio = precio * 0.5  # Descuento del 50% para menores de 15 años o mayores de 60 años
        elif edad <= 3:
            return 0  # Entrada gratuita para menores de 3 años
        return precio