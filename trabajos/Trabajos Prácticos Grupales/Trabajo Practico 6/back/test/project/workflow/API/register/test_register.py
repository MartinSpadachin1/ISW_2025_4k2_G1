import pytest
from unittest import mock
from sqlmodel import Session, select

# Asumimos que estas constantes/clases están definidas en el contexto de tu prueba
from src.common.persistance.models import Usuario 
# La constante para el hash simulado
TEST_HASH = "mocked_hashed_password_for_tests" 
TEST_EMAIL = "new_user@example.com"
TEST_PASSWORD = "password1234"




# Mockeamos hash_password para controlar el valor que se guarda en la DB
@mock.patch('src.project.workflow.API.register.register.hash_password', return_value=TEST_HASH)
def test_register_user_ok(mock_hash_password, client_con_db, session: Session):
    """
    Verifica que un usuario nuevo se registre correctamente, devuelva status 201, 
    y se guarde con el hash de contraseña correcto en la DB.
    """
    # Setup
    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }

    # Execution
    r = client_con_db.post("/user/register", json=payload)

    # Assertion 1: Respuesta de la API
    assert r.status_code == 201, f"Esperaba 201, obtuve {r.status_code}. Respuesta: {r.json()}"
    assert r.json().get("email") == TEST_EMAIL
    
    # Assertion 2: Verificación de la llamada a la función de hasheo
    # Aseguramos que la función de hasheo fue llamada con la contraseña en texto plano
    mock_hash_password.assert_called_once_with(TEST_PASSWORD)
    
    # Assertion 3: Verificación del estado en la Base de Datos
    # Buscamos el usuario recién creado en la DB
    statement = select(Usuario).where(Usuario.email == TEST_EMAIL)
    db_user = session.exec(statement).first()
    
    # Verificamos que el usuario fue guardado
    assert db_user is not None
    # Verificamos que se guardó el hash simulado, no la contraseña en texto plano
    assert db_user.hashed_password == TEST_HASH
    # Verificamos que la contraseña NO sea el texto plano
    assert db_user.hashed_password != TEST_PASSWORD


@mock.patch('src.project.workflow.API.register.register.hash_password', return_value=TEST_HASH)
def test_register_user_existing_email_fails(mock_hash_password, client_con_db, session: Session):
    """
    Verifica que el registro falle con status 400 si el email ya existe.
    """
    # Setup: Pre-insertamos el usuario directamente en la base de datos de prueba
    existing_user = Usuario(email=TEST_EMAIL, hashed_password=TEST_HASH)
    session.add(existing_user)
    session.commit()
    
    payload = {
        "email": TEST_EMAIL, # Intentamos registrar el mismo email
        "password": TEST_PASSWORD
    }

    # Execution
    r = client_con_db.post("/user/register", json=payload)

    # Assertion
    assert r.status_code == 400
    assert r.json().get("detail") == "El mail ya está registrado"
    
    # Verificamos que hash_password NO fue llamado, ya que el código debe fallar
    # en la verificación de existencia antes de intentar hashear.
    mock_hash_password.assert_not_called()

@mock.patch('src.project.workflow.API.register.register.hash_password', return_value=TEST_HASH)
def test_register_user_existing_bad_email_fails(mock_hash_password, client_con_db, session: Session):
    """
    Verifica que el registro falle con status 400 si el email ya existe.
    """
    # Setup: Pre-insertamos el usuario directamente en la base de datos de prueba
    TEST_EMAIL = "bad_email_format"
    payload = {
        "email": TEST_EMAIL, # Intentamos registrar el mismo email
        "password": TEST_PASSWORD
    }

    # Execution
    r = client_con_db.post("/user/register", json=payload)

    # Assertion
    assert r.status_code == 400
    assert r.json().get("detail") == "El mail no es válido"
    
    # Verificamos que hash_password NO fue llamado, ya que el código debe fallar
    # en la verificación de existencia antes de intentar hashear.
    mock_hash_password.assert_not_called()


