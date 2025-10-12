import pytest
from unittest import mock

from src.project.workflow.API.login.login import create_access_token 
from src.project.workflow.API.config import SECRET_KEY, ALGORITHM
from src.common.persistance.models import Usuario


TEST_PASSWORD = "password_secreta"
TEST_EMAIL = "test_user@example.com"
TEST_HASH = "fake_hashed_password_123" # Valor simulado
TEST_NAME = "Test User"


@pytest.fixture(scope="function")
def setup_user(session): # Solo necesita 'session' como argumento inyectado
    """
    Crea un usuario de prueba en la base de datos de test
    antes de cada test que lo requiera, usando un hash simulado.
    """
    
    # 1. Activación del mock DENTRO del fixture para obtener el hash simulado
    # Importante: El path debe ser donde la función hash_password es usada por el código de la app.
    # En este caso, asumimos que se usa en 'security.py' para la función que la llama.
    with mock.patch('src.project.workflow.API.login.security.hash_password', return_value=TEST_HASH):
        
        # 2. Crear la instancia del usuario
        test_user = Usuario(
            nombre= TEST_NAME,
            email=TEST_EMAIL,
            hashed_password=TEST_HASH # Usamos la constante de hash simulado
            # Añade otros campos obligatorios aquí
        )
        
        # 3. Insertar y confirmar en la sesión transaccional
        session.add(test_user)
        session.commit()
        session.refresh(test_user) 
        
        # 4. Cede el control (yield) para que el test se ejecute
        yield test_user

        # 5. La limpieza se hace automáticamente por el fixture 'session' (rollback)
        # pero es buena práctica tener la lógica de mock/contexto contenida.



@mock.patch('src.project.workflow.API.login.login.verify_password', autospec=True)
def test_login_ok_devuelve_token(mock_verify_password, client_con_db, setup_user):
    """
    Verifica que con email y contraseña correctos, el endpoint devuelva
    un token JWT con el email del usuario en el claim 'sub'.
    """
    # Setup
    mock_verify_password.return_value = True # Forzamos que la verificación sea EXITOSA
    
    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD 
    }
    
    # Execution
    r = client_con_db.post("/auth/login", json=payload)
    
    # Assertions
    assert r.status_code == 200, f"Status code inesperado: {r.status_code}. Respuesta: {r.json()}"
    
    body = r.json()
    assert "access_token" in body
    assert body.get("token_type") == "bearer"
    
    # Verificación de la llamada: Aseguramos que la verificación de contraseña fue llamada
    mock_verify_password.assert_called_once_with(TEST_PASSWORD, setup_user.hashed_password)
    
    # Necesitarás una función auxiliar para decodificar si no la tienes
    from jose import jwt
    
    token = body["access_token"]
    
    # Decodificar el token para verificar el 'sub' (subject/usuario)
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        pytest.fail(f"Fallo al decodificar el token: {e}")
        
    assert decoded_token.get("sub") == TEST_EMAIL
    assert "exp" in decoded_token


def test_login_falla_con_email_no_registrado(client_con_db):
    """Verifica que falle el login si el email no existe en la DB."""
    
    payload = {
        "email": "non_existent_user@example.com",
        "password": TEST_PASSWORD 
    }
    
    # Execution
    r = client_con_db.post("/auth/login", json=payload)

    # Assertions
    assert r.status_code == 400
    assert r.json().get("detail") == "Email o contraseña incorrectos"

@mock.patch('src.project.workflow.API.login.login.verify_password', autospec=True)
def test_login_falla_con_password_incorrecta(mock_verify_password, client_con_db, setup_user):
    """
    Verifica que falle el login si la contraseña es incorrecta (verify_password retorna False).
    """
    # Setup
    mock_verify_password.return_value = False # Forzamos que la verificación sea FALLIDA
    
    payload = {
        "email": TEST_EMAIL,
        "password": "wrong_password" 
    }
    
    # Execution
    r = client_con_db.post("/auth/login", json=payload)

    # Assertions
    assert r.status_code == 400
    assert r.json().get("detail") == "Email o contraseña incorrectos"
    
    # Verificación de la llamada
    mock_verify_password.assert_called_once()