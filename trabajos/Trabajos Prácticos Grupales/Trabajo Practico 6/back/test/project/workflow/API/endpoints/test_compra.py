from unittest import mock

from fastapi.testclient import TestClient
import pytest
from src.project.workflow.API.main import app
from src.common.entradas import VIP, REGULAR
from src.common.pago import EFECTIVO, TARJETA

client = TestClient(app)

def test_validar_compra_ok(client_con_db): 
    """
    Verifica que /validar_compra/ valide correctamente una compra válida,
    simulando un usuario autenticado con un mock.
    """
    
    # Asignamos el fixture a 'client' para mantener la lógica original del cuerpo del test
    client = client_con_db
    payload = {
        "fecha": "2099-12-02",
        # Las constantes ya están definidas como strings
        "visitantes": [{"edad": 20, "tipo_entrada": VIP}], 
        "forma_pago": EFECTIVO
    }
    
    # Execution
    r = client.post("compra/validar_compra/", json=payload)

    # Assertions
    assert r.status_code == 200, f"Status code inesperado: {r.status_code}. Respuesta: {r.json()}"
    
    body = r.json()
    
    # Verificación de la respuesta
    assert body.get("valido") is True, f"Compra válida esperada, 'valido' es False. Respuesta: {body}"
    assert "id_compra" in body, f"Falta 'id_compra' en respuesta. Respuesta: {body}"
    
def test_validar_compra_invalid_fecha(client_con_db):
    client = client_con_db

    payload = {
        "fecha": "2000-01-01",  # fecha pasada
        "visitantes": [{"edad": 20, "tipo_entrada": VIP}],
        "forma_pago": EFECTIVO
    }
    """Verifica que /validar_compra/ marque inválida una fecha pasada."""
    # Execution
    r = client.post("compra/validar_compra/", json=payload)
    assert r.status_code == 400, f"Status code inesperado: {r.status_code}"
    body = r.json()
    assert "detail" in body
    assert "La fecha no es válida según las reglas definidas" in body["detail"]


def test_validar_compra_too_many_visitantes(client_con_db):
    client = client_con_db

    payload = {
        "token": "token-valido",
        "fecha": "2099-12-02",
        "visitantes": [{"edad": 20, "tipo_entrada": VIP}] * 11,
        "forma_pago": TARJETA
    }
    r = client.post("compra/validar_compra/", json=payload)
    assert r.status_code == 400, f"Status code inesperado: {r.status_code}"
    body = r.json()
    assert "detail" in body
    assert "No se pueden incluir más de 10 visitantes por compra" in body["detail"]

def test_validar_compra_invalid_forma_pago(client_con_db):
    client = client_con_db
    payload = {
        "token": "token-valido",
        "fecha": "2099-12-02",  # fecha futura
        "visitantes": [{"edad": 20, "tipo_entrada": VIP}],
        "forma_pago": "bitcoin"  # forma de pago inválida   
    }
    r = client.post("compra/validar_compra/", json=payload)
    assert r.status_code == 400, f"Status code inesperado: {r.status_code}"
    body = r.json()
    assert "detail" in body
    assert "Forma de pago inválida" in body["detail"]