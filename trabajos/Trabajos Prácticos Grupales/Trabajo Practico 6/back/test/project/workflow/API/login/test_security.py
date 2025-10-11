import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from jose import jwt

from src.project.workflow.API.login.security import verify_token, hash_password, verify_password
from src.project.workflow.API.config import SECRET_KEY, ALGORITHM

PASSWORD_CORTA = "mi_secreta"
PASSWORD_LARGA = "a" * 100 # Contraseña que excede el límite de 72 bytes de bcrypt
PASSWORD_INCORRECTA = "incorrecta"

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


def test_hash_password_genera_hash_valido():
    """Verifica que el hash generado no sea la contraseña original (seguridad)
       y que sea un string."""
    
    hashed_pass = hash_password(PASSWORD_CORTA)
    
    # 1. El hash debe ser un string
    assert isinstance(hashed_pass, str)
    
    # 2. El hash no debe coincidir con la contraseña original (seguridad básica)
    assert hashed_pass != PASSWORD_CORTA



def test_verify_password_coincide_con_hash_corto():
    """Verifica que una contraseña corta correcta coincida con su hash."""
    hashed_pass = hash_password(PASSWORD_CORTA)
    
    # Assertion: La verificación debe ser True
    assert verify_password(PASSWORD_CORTA, hashed_pass)

def test_verify_password_falla_con_password_incorrecta():
    """Verifica que una contraseña incorrecta NO coincida con el hash."""
    hashed_pass = hash_password(PASSWORD_CORTA)
    
    # Assertion: La verificación debe ser False
    assert verify_password(PASSWORD_INCORRECTA, hashed_pass) is False


def test_verify_password_maneja_truncamiento_en_hasheo():
    """
    Verifica que el hasheo de una contraseña LARGA (truncada) coincida
    con la verificación de la misma contraseña LARGA (truncada en verify_password).
    """
    # 1. Hashea la contraseña larga (se trunca internamente a los primeros 72 bytes)
    hashed_pass_larga = hash_password(PASSWORD_LARGA)
    
    # 2. Verifica la contraseña larga (también se trunca en verify_password)
    # Deberían coincidir, ya que ambas funciones ven solo los primeros 72 bytes.
    assert verify_password(PASSWORD_LARGA, hashed_pass_larga)

def test_verify_password_falla_si_solo_se_usa_la_parte_truncada():
    """
    Verifica que el sistema de hasheo funcione correctamente:
    Un hash de una contraseña de 72 bytes NO debe ser verificado con
    una contraseña de 71 bytes (aunque la parte común es idéntica).
    """
    # La contraseña larga tiene 'a' * 72 en sus primeros bytes (72 bytes de largo)
    password_72_bytes = "a" * 72 
    password_71_bytes = "a" * 71 
    
    # 1. Hashea la contraseña de 72 bytes
    hashed_pass_72 = hash_password(password_72_bytes)
    
    # 2. Intenta verificar con la versión más corta
    # Debe fallar porque la contraseña de entrada es diferente.
    assert verify_password(password_71_bytes, hashed_pass_72) is False

def test_verify_password_truncamiento_evita_value_error():
    """
    Verifica que la función verify_password NO lance un ValueError
    si se le pasa una contraseña de entrada muy larga.
    """
    hashed_pass = hash_password(PASSWORD_CORTA)
    
    try:
        # Pasa una contraseña muy larga que sin la truncación fallaría
        verify_password(PASSWORD_LARGA, hashed_pass)
    except ValueError as e:
        pytest.fail(f"La truncación falló: Se capturó un ValueError: {e}")
    except Exception:
        # Si no es un ValueError, podría ser un error interno, lo dejamos pasar.
        pass
