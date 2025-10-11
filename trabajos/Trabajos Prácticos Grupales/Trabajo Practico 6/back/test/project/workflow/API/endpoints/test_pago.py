import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.project.workflow.API.main import app

import pytest
from src.common.pago import EFECTIVO  # si tenés constantes de pago
from datetime import date

client = TestClient(app)

def test_procesar_pago_ok(client_con_db):
    """
    Verifica que /procesar_pago/ procese correctamente un pago válido,
    usando un token mockeado y la base de datos en memoria.
    """

    client = client_con_db
    payload = {
        "id_reserva": 1,
        "numero_tarjeta": "1234567812345678",
        "cvv": "123",
        "fecha_expiracion": "2099-12-31"  # Fecha futura válida
    }

    r = client.post("/pago/procesar_pago/", json=payload)

    # Assertions
    assert r.status_code == 200, f"Status code inesperado: {r.status_code}. Respuesta: {r.json()}"
    body = r.json()

    # Validación de campos en la respuesta
    assert body.get("message") == "Pago procesado exitosamente"
    assert body.get("email") == "test@example.com"
    assert body.get("data") == payload


def test_procesar_pago_invalido(client_con_db):
    """
    Verifica que /procesar_pago/ falle cuando se envía una tarjeta inválida.
    """

    client = client_con_db
    payload = {
        "id_reserva": 1,
        "numero_tarjeta": "abc",  # Tarjeta inválida
        "cvv": "xxx",             # CVV inválido
        "fecha_expiracion": "2020-01-01"  # Fecha expirada
    }

    r = client.post("/pago/procesar_pago/", json=payload)

    assert r.status_code == 400, f"Se esperaba 400, se obtuvo {r.status_code}. Respuesta: {r.json()}"
    body = r.json()
    assert body.get("detail") == "Datos de pago inválidos"