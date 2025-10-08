import pytest

from src.common.entradas import VIP, GENERAL
from src.project.entities.Visitante import Visitante
from src.project.workflow.compra import calcular_monto

@pytest.mark.parametrize("visitantes, expected_monto", [
    ([Visitante(20, VIP), Visitante(25, VIP)], 20000),
    ([Visitante(30, GENERAL)], 5000),
    ([Visitante(10, VIP), Visitante(66, GENERAL)], 7500),
    ([Visitante(2, GENERAL)], 0)
])
def test_calcular_monto_ok(visitantes, expected_monto):
    monto = calcular_monto(visitantes)

    assert monto == expected_monto, f"El monto calculado es {monto}, pero se esperaba {expected_monto}"

def test_calcular_monto_error():
    with pytest.raises(ValueError):
        calcular_monto([])
    with pytest.raises(ValueError):
        calcular_monto([Visitante(20, VIP)] * 11)