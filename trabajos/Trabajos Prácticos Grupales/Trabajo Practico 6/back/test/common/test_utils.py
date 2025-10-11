import pytest
from src.common.utils import validar_fecha
from src.common.utils import validar_mail
from src.common.utils import validar_pago
from datetime import date, datetime, timedelta
import re
from unittest.mock import patch




def test_validar_fecha_anterior():
    # Setup
    ayer = date.today() - timedelta(days=1)
    # Execution
    resultado = validar_fecha(ayer)
    # Assertion
    assert resultado is False, f"La fecha {ayer} es anterior a hoy, debería devolver False"


def test_validar_fecha_lunes():
    # Setup
    hoy = date.today()
    dias_hasta_lunes = (0 - hoy.weekday()) % 7
    if dias_hasta_lunes == 0:
        dias_hasta_lunes = 7
    proximo_lunes = hoy + timedelta(days=dias_hasta_lunes)
    assert proximo_lunes.weekday() == 0, f"Cálculo de próximo lunes incorrecto: {proximo_lunes}"
    # Execution
    resultado = validar_fecha(proximo_lunes)
    # Assertion
    assert resultado is False, f"El próximo lunes {proximo_lunes} debe ser inválido (lunes)"


def test_validar_fecha_navidad():
    # Setup
    year = date.today().year
    navidad = date(year, 12, 25)
    if navidad < date.today():
        navidad = date(year + 1, 12, 25)
    # Execution
    resultado = validar_fecha(navidad)
    # Assertion
    assert resultado is False, f"La fecha {navidad} (Navidad) debe ser inválida"


def test_validar_fecha_ano_nuevo():
    # Setup
    year = date.today().year
    primer_enero = date(year, 1, 1)
    if primer_enero < date.today():
        primer_enero = date(year + 1, 1, 1)
    # Execution
    resultado = validar_fecha(primer_enero)
    # Assertion
    assert resultado is False, f"La fecha {primer_enero} (Año Nuevo) debe ser inválida"


def test_validar_fecha_valida():
    # Setup
    manana = date.today() + timedelta(days=1)
    while manana.weekday() == 0 or (manana.month, manana.day) in ((12, 25), (1, 1)):
        manana += timedelta(days=1)
    # Execution
    resultado = validar_fecha(manana)
    # Assertion
    assert resultado is True, f"La fecha {manana} debería ser válida según las reglas"


def test_validar_fecha_excepciones_raise():
    # Execution / Assertion: formato inválido
    with pytest.raises(ValueError, match="formato inválido"):
        validar_fecha("2025-13-40")
    # Execution / Assertion: tipo inválido
    with pytest.raises(TypeError, match="parámetro fecha debe ser"):
        validar_fecha(12345)




# Asume que esta importación funciona:
# from tu_modulo_de_utilidades import validar_mail 

# Casos de prueba: (email, resultado_esperado)
test_cases = [
    # --- Casos Válidos (True) ---
    ("usuario@dominio.com", True),
    ("user.name123@sub.domain-test.net", True),
    ("a@b.co", True), 
    ("first-last@longdomain.technology", True), 
    ("with+plus@example.com", True), 
    ("underscore_@server.info", True),
    
    # --- Casos Inválidos (False) ---

    ("solo.dominio.com", False), 
    ("usuario@dominio", False), 
    ("@dominio.com", False),
    ("usuario@.com", False), 
    ("user,name@domain.com", False),
    ("user@domain:80.com", False), 
    ("user@domain!", False), 
    ("usuario@dominio.c", False), 
    (" user@domain.com", False), 
    ("user@domain.com ", False), 
]

@pytest.mark.parametrize("email, expected_result", test_cases)
def test_validar_mail_parametrized(email, expected_result):
    """
    Prueba la función validar_mail con una variedad de formatos válidos e inválidos.
    """
    # Execution
    actual_result = validar_mail(email)
    
    # Assertion
    assert actual_result == expected_result, \
        f"Fallo para el email '{email}'. Resultado esperado: {expected_result}, Resultado obtenido: {actual_result}"


MOCK_TODAY_DATE = date(2025, 3, 10) 

@patch('datetime.datetime', autospec=True)
@pytest.mark.parametrize("numero, cvv, fecha_expiracion, expected_result, test_case", [
    # --- Casos de Éxito (True) ---
    # Tarjeta de 16 dígitos, CVV de 3, fecha futura (2025-12-01)
    ("1234567890123456", "123", "2025-12-01", True, "Tarjeta 16, CVV 3, Fecha OK"),
    # Tarjeta de 16 dígitos, CVV de 4, fecha futura (2030-01-01)
    ("9876543210987654", "4321", "2030-01-01", True, "Tarjeta 16, CVV 4, Fecha OK"),
    
    # --- Fallos en Número de Tarjeta (False) ---
    ("123456789012345", "123", "2030-01-01", False, "Número corto (15 dígitos)"),
    ("12345678901234567", "123", "2030-01-01", False, "Número largo (17 dígitos)"),
    ("123456789012345A", "123", "2030-01-01", False, "Número con letra"),
    
    # --- Fallos en CVV (False) ---
    ("1234567890123456", "12", "2030-01-01", False, "CVV corto (2 dígitos)"),
    ("1234567890123456", "12345", "2030-01-01", False, "CVV largo (5 dígitos)"),
    ("1234567890123456", "12A", "2030-01-01", False, "CVV con letra"),
    
    # --- Fallos en Fecha de Expiración (Fecha Pasada o Hoy) (False) ---
    ("1234567890123456", "123", "2025-01-01", False, "Fecha pasada (Enero 2025)"),
    ("1234567890123456", "123", "2024-12-31", False, "Fecha pasada (Año anterior)"),
    ("1234567890123456", "123", "2025-03-10", False, "Fecha de hoy (Igual a MOCK_TODAY_DATE)"),
    
    # --- Fallos en Formato de Fecha (False) ---
    ("1234567890123456", "123", "12/25", False, "Formato incorrecto (MM/YY)"),
    ("1234567890123456", "123", "2025-13-01", False, "Mes inválido"),
])
def test_validar_pago_parametrized(mock_datetime, numero, cvv, fecha_expiracion, expected_result, test_case):
    """
    Prueba que la función de validación de pago maneje correctamente los formatos y la fecha de expiración.
    """
    # Configurar el mock de la fecha actual
    # Hacemos que datetime.datetime.today().date() siempre devuelva la fecha mockeada
    mock_datetime.today.return_value = MOCK_TODAY_DATE
    
    # Execution
    # Importante: La función debe estar accesible aquí.
    # Si la función está en el mismo archivo de prueba, puedes llamarla directamente.
    actual_result = validar_pago(numero, cvv, fecha_expiracion)
    
    # Assertion
    assert actual_result == expected_result, \
        f"Fallo en caso: '{test_case}'. Esperado: {expected_result}, Obtenido: {actual_result}"