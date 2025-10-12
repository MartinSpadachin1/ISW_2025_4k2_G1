import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.project.workflow.API.main import app

import pytest
from src.common.pago import EFECTIVO  # si tenés constantes de pago
from src.common.persistance.models import Reserva
from datetime import date

client = TestClient(app)

def test_procesar_pago_ok(client_con_db, session):
    """
    Verifica que /procesar_pago/ procese correctamente un pago válido,
    usando un token mockeado y la base de datos en memoria.
    """

    client = client_con_db

    # Crear una reserva de prueba en la DB en memoria para este test
    nueva_reserva = Reserva(mail="test@example.com", fecha=str(date.today()), tipo_pago="efectivo")
    session.add(nueva_reserva)
    session.commit()
    session.refresh(nueva_reserva)

    payload = {
        "id_reserva": nueva_reserva.id,
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


def test_procesar_pago_invalido(client_con_db, session):
    """
    Verifica que /procesar_pago/ falle cuando se envía una tarjeta inválida.
    """

    client = client_con_db

    # Crear reserva para este test también
    nueva_reserva = Reserva(mail="test@example.com", fecha=str(date.today()), tipo_pago="efectivo")
    session.add(nueva_reserva)
    session.commit()
    session.refresh(nueva_reserva)

    payload = {
        "id_reserva": nueva_reserva.id,
        "numero_tarjeta": "abc",  # Tarjeta inválida
        "cvv": "xxx",             # CVV inválido
        "fecha_expiracion": "2020-01-01"  # Fecha expirada
    }

    r = client.post("/pago/procesar_pago/", json=payload)

    assert r.status_code == 400, f"Se esperaba 400, se obtuvo {r.status_code}. Respuesta: {r.json()}"
    body = r.json()
    assert body.get("detail") == "Datos de pago inválidos"