import pytest

from src.common.entradas import VIP, GENERAL
from src.project.entities.Visitante import Visitante
from src.project.workflow.compra_calculo import calcular_monto

@pytest.mark.parametrize("visitantes, expected_monto", [
    ([Visitante(20, VIP), Visitante(25, VIP)], 20000),
    ([Visitante(30, GENERAL)], 5000),
    ([Visitante(10, VIP), Visitante(66, GENERAL)], 7500),
    ([Visitante(2, GENERAL)], 0)
])
def test_calcular_monto_ok(visitantes, expected_monto):
    """Valida cálculos correctos de montos para combinaciones de visitantes."""
    # Setup
    input_visitantes = visitantes
    # Execution
    monto = calcular_monto(input_visitantes)
    # Assertion
    assert monto == expected_monto, f"El monto calculado es {monto}, pero se esperaba {expected_monto}"

def test_calcular_monto_error():
    """Verifica que se lancen errores para entradas inválidas (lista vacía y >10 visitantes)."""
    # Execution / Assertion: lista vacía
    with pytest.raises(ValueError, match="vacía"):
        calcular_monto([])
    # Execution / Assertion: más de 10 visitantes
    with pytest.raises(ValueError, match="No se pueden procesar más de 10 visitantes"):
        calcular_monto([Visitante(20, VIP)] * 11)