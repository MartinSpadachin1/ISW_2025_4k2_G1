from fastapi.testclient import TestClient
import pytest
from src.project.workflow.API.main import app
from src.common.entradas import VIP, GENERAL
from src.common.pago import EFECTIVO, TARJETA

client = TestClient(app)

def test_obtener_monto_total():
    """Comprueba que el endpoint /monto/ calcula el total correctamente para varios visitantes."""
    # Setup
    payload = {"visitantes": [{"edad": 20, "tipo_entrada": VIP}, {"edad": 25, "tipo_entrada": GENERAL}]}
    # Execution
    r = client.post("monto/monto_total/", json=payload)
    # Assertion
    assert r.status_code == 200, f"Status code inesperado: {r.status_code}"
    assert r.json() == 15000, f"Respuesta esperada 15000, obtuvo {r.json()}"


def test_obtener_monto_unico():
    """Comprueba que /monto_unico/ devuelve el monto de un único visitante."""
    # Setup
    payload = {"edad": 4, "tipo_entrada": VIP}
    # Execution
    r = client.post("monto/monto_unico/", json=payload)
    # Assertion
    assert r.status_code == 200, f"Status code inesperado: {r.status_code}"
    assert isinstance(r.json(), (int, float)), f"El monto debe ser numérico, obtuvo: {r.json()}"


def test_obtener_edades():
    """Comprueba que /edades/ devuelva las categorías esperadas."""
    # Execution
    r = client.get("monto/edades/")
    # Assertion
    assert r.status_code == 200, f"Status code inesperado: {r.status_code}"
    data = r.json()
    assert "bebes" in data and "niños" in data and "adultos" in data and "adulto_mayor" in data, f"Respuesta inesperada en /edades/: {data}"

