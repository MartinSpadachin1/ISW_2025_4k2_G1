import pytest
from src.common.entrada import Entrada

class TestEntrada:
    @pytest.fixture
    def test_calcular_precio_entrada(self):
        print("hola")
        e1 = Entrada(15, False)
        assert e1.get_precio() == 2500
