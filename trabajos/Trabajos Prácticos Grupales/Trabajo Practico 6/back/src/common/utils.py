import datetime
from typing import Union
import re

def validar_mail(mail: str) -> bool:
    """
    Realiza una validación de email más robusta usando una expresión regular.

    Args:
        mail (str): La cadena de email a validar.

    Returns:
        bool: True si el email tiene un formato válido, False en caso contrario.
    """
    # Expresión regular estándar para la mayoría de los formatos de email válidos.
    # Cubre caracteres alfanuméricos, puntos, guiones y el formato local@dominio.tld
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # re.fullmatch() intenta hacer coincidir el patrón con toda la cadena.
    # Si encuentra una coincidencia, devuelve un objeto match (True); de lo contrario, devuelve None (False).
    return bool(re.fullmatch(regex, mail))

def validar_fecha(fecha: Union[str, datetime.date]) -> bool:
    """
    Valida una fecha recibida como string ISO (YYYY-MM-DD) o datetime.date.
    Reglas de validación:
    - No puede ser anterior a la fecha de hoy.
    - No puede ser un lunes.
    - No puede ser Navidad (25/12) ni Año Nuevo (01/01).

    Retorna True si la fecha es válida, False en caso contrario.
    """
    # Normalizar a datetime.date
    if isinstance(fecha, str):
        try:
            fecha_obj = datetime.date.fromisoformat(fecha)
        except Exception:
            raise ValueError("Fecha con formato inválido. Use YYYY-MM-DD o un objeto datetime.date")
    elif isinstance(fecha, datetime.date):
        fecha_obj = fecha
    else:
        raise TypeError("El parámetro fecha debe ser str (YYYY-MM-DD) o datetime.date")

    hoy = datetime.date.today()
    if fecha_obj < hoy:
        return False

    # weekday(): Monday == 0
    if fecha_obj.weekday() == 0:
        return False

    # Navidad y Año Nuevo
    if (fecha_obj.month, fecha_obj.day) in ((12, 25), (1, 1)):
        return False

    return True


def validar_token(token: str) -> bool:
    return True # Placeholder para validación de token, siempre devuelve True

