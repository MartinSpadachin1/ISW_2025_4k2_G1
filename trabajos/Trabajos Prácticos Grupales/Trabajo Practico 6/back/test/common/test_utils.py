import datetime
import pytest
from src.common.utils import validar_fecha
from src.common.utils import validar_mail

def test_validar_fecha_anterior():
    # Setup
    ayer = datetime.date.today() - datetime.timedelta(days=1)
    # Execution
    resultado = validar_fecha(ayer)
    # Assertion
    assert resultado is False, f"La fecha {ayer} es anterior a hoy, debería devolver False"


def test_validar_fecha_lunes():
    # Setup
    hoy = datetime.date.today()
    dias_hasta_lunes = (0 - hoy.weekday()) % 7
    if dias_hasta_lunes == 0:
        dias_hasta_lunes = 7
    proximo_lunes = hoy + datetime.timedelta(days=dias_hasta_lunes)
    assert proximo_lunes.weekday() == 0, f"Cálculo de próximo lunes incorrecto: {proximo_lunes}"
    # Execution
    resultado = validar_fecha(proximo_lunes)
    # Assertion
    assert resultado is False, f"El próximo lunes {proximo_lunes} debe ser inválido (lunes)"


def test_validar_fecha_navidad():
    # Setup
    year = datetime.date.today().year
    navidad = datetime.date(year, 12, 25)
    if navidad < datetime.date.today():
        navidad = datetime.date(year + 1, 12, 25)
    # Execution
    resultado = validar_fecha(navidad)
    # Assertion
    assert resultado is False, f"La fecha {navidad} (Navidad) debe ser inválida"


def test_validar_fecha_ano_nuevo():
    # Setup
    year = datetime.date.today().year
    primer_enero = datetime.date(year, 1, 1)
    if primer_enero < datetime.date.today():
        primer_enero = datetime.date(year + 1, 1, 1)
    # Execution
    resultado = validar_fecha(primer_enero)
    # Assertion
    assert resultado is False, f"La fecha {primer_enero} (Año Nuevo) debe ser inválida"


def test_validar_fecha_valida():
    # Setup
    manana = datetime.date.today() + datetime.timedelta(days=1)
    while manana.weekday() == 0 or (manana.month, manana.day) in ((12, 25), (1, 1)):
        manana += datetime.timedelta(days=1)
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