import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from src.common.persistance.database import get_session
from src.common.persistance.models import Usuario
from src.project.workflow.API.login.security import verify_token
from src.project.workflow.API.main import app
from unittest import mock

# --- 1. Definición del Fixture de Base de Datos ---
# Se utiliza una base de datos SQLite en memoria para tests rápidos y aislados.
@pytest.fixture(scope="session")
def engine_test():
    """Crea un motor de base de datos SQLite en memoria, ideal para tests rápidos."""
    # CLAVE: Añadir connect_args para deshabilitar la comprobación de hilos de SQLite
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False} 
    )

# 2. Configuración y Limpieza de la BD
@pytest.fixture(scope="session", autouse=True)
def setup_db(engine_test):
    """Crea las tablas antes de todos los tests y las elimina al finalizar."""
    # Crea todas las tablas en la BD en memoria
    SQLModel.metadata.create_all(engine_test)
    yield
    # Limpia (elimina todas las tablas) al finalizar la sesión de pruebas
    SQLModel.metadata.drop_all(engine_test)

# 3. Fixture de Sesión Transaccional
# Proporciona una sesión a cada test. Usa rollback al final para aislar los tests.
@pytest.fixture(scope="function")
def session(engine_test):
    """Proporciona una sesión de BD transaccional que hace rollback automáticamente."""
    
    # 1. Conexión y Transacción: Crea una nueva conexión y empieza una transacción
    connection = engine_test.connect()
    transaction = connection.begin()
    
    # 2. Sesión para el test: Crea una sesión vinculada a la conexión transaccional
    db = Session(bind=connection)

    # Sobrescribimos la dependencia en la aplicación para que use esta sesión
    def override_get_session():
        yield db
    
    def override_verify_token():
        return "test@example.com"
    
    # Asegura que la aplicación use la sesión de test para este test
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[verify_token] = override_verify_token

    try:
        # Pasa la sesión al test
        yield db
    finally:
        # 3. Limpieza: 
        # Cierra la sesión, revierte la transacción (borra cambios del test)
        db.close()
        transaction.rollback()
        connection.close()
        # Restaura la dependencia original (aunque no siempre es necesario)
        del app.dependency_overrides[get_session]
        del app.dependency_overrides[verify_token]

# --- Fixture del Cliente de Test ---
# ¡Este es el fixture que tu test necesita!
@pytest.fixture(scope="function")
def client_con_db(session):
    """Crea el TestClient de FastAPI que usa la BD de test."""
    # El TestClient utiliza la 'app' que tiene la dependencia get_session sobrescrita.
    return TestClient(app)

TEST_HASH = "fake_hashed_password_123" # Valor simulado

