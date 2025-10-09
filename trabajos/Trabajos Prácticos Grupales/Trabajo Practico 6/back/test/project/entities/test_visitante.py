from src.project.entities.Visitante import Visitante
from src.common.entradas import VIP, GENERAL, PRECIO_VIP, PRECIO_GENERAL


def test_visitante_bebe_gratis():
    """Comprueba que un bebé de 2 años paga 0."""
    # Setup
    v = Visitante(2, GENERAL)
    # Execution
    monto = v.monto
    # Assertion
    assert monto == 0, f"Bebé de 2 años debe pagar 0, obtuvo {monto}"


def test_visitante_nino_vip_descuento():
    """Verifica descuento 50% para niño con entrada VIP."""
    # Setup
    v = Visitante(10, VIP)
    expected = PRECIO_VIP * 0.5
    # Execution
    monto = v.monto
    # Assertion
    assert monto == expected, f"Niño VIP debe pagar {expected}, obtuvo {monto}"


def test_visitante_adulto_general():
    """Verifica que un adulto pague el precio general sin descuento."""
    # Setup
    v = Visitante(30, GENERAL)
    expected = PRECIO_GENERAL
    # Execution
    monto = v.monto
    # Assertion
    assert monto == expected, f"Adulto general debe pagar {expected}, obtuvo {monto}"


def test_visitante_adulto_mayor_vip():
    """Verifica descuento 50% para adulto mayor con entrada VIP."""
    # Setup
    v = Visitante(70, VIP)
    expected = PRECIO_VIP * 0.5
    # Execution
    monto = v.monto
    # Assertion
    assert monto == expected, f"Adulto mayor VIP debe pagar {expected}, obtuvo {monto}"


def test_visitante_atributos():
    """Comprueba atributos `edad` y `tipo_entrada` de la instancia."""
    # Setup
    v = Visitante(25, GENERAL)
    # Execution / Assertion
    assert v.edad == 25, f"Edad esperada 25, obtuvo {v.edad}"
    assert v.tipo_entrada == GENERAL, f"Tipo de entrada esperado {GENERAL}, obtuvo {v.tipo_entrada}"

def test_visitante_edad_invalida_negativa():
    """Lanza ValueError si la edad es negativa."""
    # Execution / Assertion
    with __import__('pytest').raises(ValueError) as exc:
        Visitante(-5, VIP)
    assert "La edad debe estar entre 0 y 120 años." in str(exc.value), f"Mensaje de error inesperado: {exc.value}"
        
def test_visitante_edad_invalida_alta():
    """Lanza ValueError si la edad es mayor al límite aceptado."""
    # Execution / Assertion
    with __import__('pytest').raises(ValueError) as exc:
        Visitante(130, GENERAL)
    assert "La edad debe estar entre 0 y 120 años." in str(exc.value), f"Mensaje de error inesperado: {exc.value}"
        
def test_visitante_edad_invalida_none():
    """Lanza ValueError si la edad es None."""
    # Execution / Assertion
    with __import__('pytest').raises(ValueError) as exc:
        Visitante(None, VIP)
    assert "La edad debe estar entre 0 y 120 años." in str(exc.value), f"Mensaje de error inesperado: {exc.value}"
        
        