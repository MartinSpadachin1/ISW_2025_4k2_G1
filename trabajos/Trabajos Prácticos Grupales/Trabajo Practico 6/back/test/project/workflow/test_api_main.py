from fastapi.testclient import TestClient
from src.project.workflow.API.main import app
from src.common.entradas import VIP, GENERAL
from src.common.pago import EFECTIVO, TARJETA

client = TestClient(app)


def test_monto():
    """Comprueba que el endpoint /monto/ calcula el total correctamente para varios visitantes."""
    # Setup
    payload = {"visitantes": [{"edad": 20, "tipo_entrada": VIP}, {"edad": 25, "tipo_entrada": GENERAL}]}
    # Execution
    r = client.post("/monto/", json=payload)
    # Assertion
    assert r.status_code == 200, f"Status code inesperado: {r.status_code}"
    assert r.json() == 15000, f"Respuesta esperada 15000, obtuvo {r.json()}"


def test_monto_unico():
    """Comprueba que /monto_unico/ devuelve el monto de un único visitante."""
    # Setup
    payload = {"edad": 4, "tipo_entrada": VIP}
    # Execution
    r = client.post("/monto_unico/", json=payload)
    # Assertion
    assert r.status_code == 200, f"Status code inesperado: {r.status_code}"
    assert isinstance(r.json(), (int, float)), f"El monto debe ser numérico, obtuvo: {r.json()}"


def test_menor_edad():
    """Comprueba que /menor_edad/ devuelva las categorías esperadas."""
    # Execution
    r = client.get("/menor_edad/")
    # Assertion
    assert r.status_code == 200, f"Status code inesperado: {r.status_code}"
    data = r.json()
    assert "bebes" in data and "niños" in data and "adultos" in data and "adulto_mayor" in data, f"Respuesta inesperada en /menor_edad/: {data}"


def test_validar_compra_ok():
    payload = {
        "token": "token-valido",
        "fecha": "2099-12-02",
        "visitantes": [{"edad": 20, "tipo_entrada": VIP}],
        "forma_pago": EFECTIVO
    }
    """Verifica que /validar_compra/ valide correctamente una compra válida."""
    # Execution
    r = client.post("/validar_compra/", json=payload)
    assert r.status_code == 200, f"Status code inesperado: {r.status_code}"
    body = r.json()
    assert body.get("valido") is True, f"Compra válida esperada, respuesta: {body}"
    assert "id_compra" in body, f"Falta id_compra en respuesta: {body}"


def test_validar_compra_invalid_fecha():
    payload = {
        "token": "token-valido",
        "fecha": "2000-01-01",  # fecha pasada
        "visitantes": [{"edad": 20, "tipo_entrada": VIP}],
        "forma_pago": EFECTIVO
    }
    """Verifica que /validar_compra/ marque inválida una fecha pasada."""
    # Execution
    r = client.post("/validar_compra/", json=payload)
    assert r.status_code == 200, f"Status code inesperado: {r.status_code}"
    body = r.json()
    assert body.get("valido") is False, f"Compra inválida esperada por fecha pasada, respuesta: {body}"


def test_validar_compra_too_many_visitantes():
    payload = {
        "token": "token-valido",
        "fecha": "2099-12-02",
        "visitantes": [{"edad": 20, "tipo_entrada": VIP}] * 11,
        "forma_pago": TARJETA
    }
    r = client.post("/validar_compra/", json=payload)
    assert r.status_code == 200, f"Status code inesperado: {r.status_code}"
    body = r.json()
    assert body.get("valido") is False, f"Compra inválida esperada por exceso de visitantes, respuesta: {body}"

def test_validar_compra_invalid_forma_pago():
    payload = {
        "token": "token-valido",
        "fecha": "2099-12-02",  # fecha futura
        "visitantes": [{"edad": 20, "tipo_entrada": VIP}],
        "forma_pago": "bitcoin"  # forma de pago inválida   
    }
    r = client.post("/validar_compra/", json=payload)
    assert r.status_code == 200, f"Status code inesperado: {r.status_code}"
    body = r.json()
    assert body.get("valido") is False, f"Compra inválida esperada por forma de pago inválida, respuesta: {body}"