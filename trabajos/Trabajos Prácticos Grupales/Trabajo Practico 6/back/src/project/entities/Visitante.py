from src.common.entradas import VIP, REGULAR, PRECIO_REGULAR, PRECIO_VIP


class Visitante: 
    """Clase que representa a un visitante con su edad, tipo de entrada y monto a pagar."""
    def __init__(self, edad: int, tipo_entrada: str):
        """Inicializa un visitante con su edad, tipo de entrada y calcula el monto a pagar."""
        self.edad = edad
        if not self.validar_edad():
            raise ValueError("La edad debe estar entre 0 y 120 años.")
        self.tipo_entrada = tipo_entrada
        self.monto = self.calcular_monto(edad, tipo_entrada)

    def calcular_monto(self, edad: int, tipo_entrada: str) -> float:
        """Calcula el monto a pagar según la edad y el tipo de entrada."""
        # Validar tipo_entrada
        if tipo_entrada == VIP:
            precio = PRECIO_VIP  # Precio base para entrada VIP
        elif tipo_entrada == REGULAR:
            precio = PRECIO_REGULAR  # Precio base para entrada REGULAR
        else:
            raise ValueError(f"Tipo de entrada inválido: {tipo_entrada}")

        if (edad < 15 or edad >= 60) and edad > 3:
            precio = precio * 0.5  # Descuento del 50% para menores de 15 años o mayores de 60 años
        elif edad <= 3:
            return 0  # Entrada gratuita para menores de 3 años
        return precio
    
    
    def validar_edad(self) -> bool:
        """Valida que la edad esté en el rango permitido (0-120 años)."""
        if self.edad is None:
            raise ValueError("La edad debe estar entre 0 y 120 años.")
        if not (0 <= self.edad <= 120):
            return False
        return True
    
    def __str__(self):
        return f"Visitante(edad={self.edad}, tipo_entrada='{self.tipo_entrada}', monto={self.monto})"