import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from jose import jwt

from src.project.workflow.API.login.security import SECRET_KEY, ALGORITHM, verify_token


def create_app():
    app = FastAPI()

    @app.get('/_test_verify')
    def _test(user: str = Depends(verify_token)):
        return {"user": user}

    return app


def make_token(payload: dict, key: str = SECRET_KEY, alg: str = ALGORITHM):
    return jwt.encode(payload, key, algorithm=alg)


def test_verify_token_valid():
    """Setup: crear token con claim sub; Execution: llamar endpoint con Authorization; Assertion: devuelve el sub."""
    app = create_app()
    client = TestClient(app)

    token = make_token({"sub": "test@example.com"})
    r = client.get('/_test_verify', headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, f"Esperaba 200 con token válido, obtuvo {r.status_code}"
    assert r.json().get('user') == 'test@example.com', f"El usuario retornado no coincide: {r.json()}"


def test_verify_token_invalid():
    """Setup: token firmado con clave incorrecta; Execution: llamar endpoint; Assertion: 401."""
    app = create_app()
    client = TestClient(app)

    bad_token = make_token({"sub": "test@example.com"}, key='wrong_key')
    r = client.get('/_test_verify', headers={"Authorization": f"Bearer {bad_token}"})
    assert r.status_code == 401, f"Esperaba 401 con token inválido, obtuvo {r.status_code} y body {r.text}"


def test_verify_token_missing_sub():
    """Setup: token válido pero sin claim sub; Execution: llamar endpoint; Assertion: dependency retorna None y endpoint devuelve user: null."""
    app = create_app()
    client = TestClient(app)

    token = make_token({"some": "claim"})
    r = client.get('/_test_verify', headers={"Authorization": f"Bearer {token}"})
    # The dependency returns payload.get('sub') which will be None if missing
    assert r.status_code == 200, f"Esperaba 200 incluso si sub falta (devuelve null), obtuvo {r.status_code}"
    assert r.json().get('user') is None, f"Esperaba user null cuando falta sub, obtuvo {r.json()}"
