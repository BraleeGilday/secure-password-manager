import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from models import Base
from database import get_db
from main import app

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function", autouse=True)
def override_db(db):
    def _get_db_override():
        yield db

    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# --- admin token fixture ---
@pytest.fixture
def token(client):
    test_admin = {
        "username": "testadmin1",
        "password": "testpassword",
        "is_admin": True,
    }
    client.post("/spm/admin/register", json=test_admin)
    data = {"username": "testadmin1", "password": "testpassword"}

    response = client.post("/spm/admin/login", data=data)

    return response.json()["access_token"]


# --- pwd generator fixtures ---
@pytest.fixture()
def test_symbols():
    return "~!@#$%^&*()-_+=,.?:;"


@pytest.fixture()
def count_characters(test_symbols):
    """
    counter helper (move to conftest.py?)
    """
    def _count(pwd):
        symbols = 0
        numbers = 0
        lowers = 0
        uppers = 0

        for c in pwd:
            if c in test_symbols:
                symbols += 1
            elif c.isdigit():
                numbers += 1
            elif c.islower():
                lowers += 1
            elif c.isupper():
                uppers += 1

        return symbols, numbers, lowers, uppers
    return _count
