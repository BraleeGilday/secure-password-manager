import pytest
from fastapi.testclient import TestClient
from main import app

# from database import LocalSession

client_401 = TestClient(app)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def registered_user(client):
    # email prefix becomes username (unless your unique-username logic appends a number)
    email = "testuser1@example.com"
    password = "testpassword"

    response = client.post(
        "/spm/user/register", json={"email": email, "password": password}
    )
    assert response.status_code == 200

    data = response.json()
    return {
        "id": data["id"],
        "email": data["email"],
        "username": data["username"],
        "password": password,  # plaintext for login (since I'm not currently sending it in response)
    }


@pytest.fixture
def token(client, registered_user):
    # OAuth2PasswordRequestForm (form encoded)
    response = client.post(
        "/spm/user/login",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_register_user(client):
    data = {"email": "newuser@example.com", "password": "pw123"}
    response = client.post("/spm/user/register", json=data)
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert body["email"] == "newuser@example.com"
    assert "username" in body


def test_login_user_gets_token(client, registered_user):
    response = client.post(
        "/spm/user/login",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert body["username"] == registered_user["username"]


def test_login_wrong_password_401(client, registered_user):
    response = client.post(
        "/spm/user/login",
        data={"username": registered_user["username"], "password": "wrong"},
    )
    assert response.status_code == 401


def test_read_user_requires_auth(client, registered_user):
    response = client.get(f"/spm/user/{registered_user['id']}")
    assert response.status_code == 401


def test_read_user_success(client, registered_user, token):
    response = client.get(
        f"/spm/user/{registered_user['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == registered_user["id"]
    assert body["email"] == registered_user["email"]
    assert body["username"] == registered_user["username"]


def test_update_user_success(client, registered_user, token):
    response = client.patch(
        f"/spm/user/{registered_user['id']}",
        json={"email": "updated@example.com"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "updated@example.com"


def test_delete_user_success(client, registered_user, token):
    response = client.delete(
        f"/spm/user/{registered_user['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204
