import os
import sys
from pathlib import Path

# Asegura que el paquete `app` sea importable desde backend/
sys.path.insert(0, str(Path(__file__).parent.parent))

# Credenciales fijas para tests (deben estar antes del primer import de app)
os.environ.setdefault("ADMIN_USER", "test@gap.cl")
os.environ.setdefault("ADMIN_PASS", "mvp1234")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DB_URL = "sqlite:///./test_temp.db"
_test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
_TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)


@pytest.fixture(scope="session", autouse=True)
def _create_test_tables():
    Base.metadata.create_all(bind=_test_engine)
    yield
    Base.metadata.drop_all(bind=_test_engine)
    _test_engine.dispose()
    db_file = Path("test_temp.db")
    if db_file.exists():
        db_file.unlink()


@pytest.fixture
def db():
    session = _TestingSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# Credenciales de prueba para pasar en cada request
AUTH = ("test@gap.cl", "mvp1234")
