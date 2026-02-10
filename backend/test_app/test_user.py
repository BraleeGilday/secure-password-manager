from test_app.fixtures.user_fixtures import registered_user, user_token
from user.user_router import MAX_LOGIN_ATTEMPTS

import uuid


# Test CREATE
def test_register_user(client):
    suffix = uuid.uuid4().hex[:8]

    email = f"user_{suffix}@example.com"

    response = client.post(
        "/spm/user/register",
        json={
            "email": email,
            "password": "password123%",
        },
    )
    assert response.status_code == 200, response.text

    body = response.json()
    assert "id" in body
    assert "display_name" in body
    assert body["email"] == email


def test_login_user_gets_token(client, registered_user):
    response = client.post(
        "/spm/user/login",
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200, response.text

    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert body["username"] == registered_user["email"]


def test_login_wrong_password_401(client, registered_user):
    response = client.post(
        "/spm/user/login",
        data={"username": registered_user["email"], "password": "wrong"},
    )
    assert response.status_code == 401


def test_login_increments_attempts(client, registered_user):
    email = registered_user["email"]

    for i in range(MAX_LOGIN_ATTEMPTS):
        response = client.post(
            "/spm/user/login",
            data={"username": email, "password": f"wrong{i}"},
        )
        assert response.status_code == 401, response.text  # Unauthorized

    response = client.post(
        "/spm/user/login",
        data={"username": email, "password": f"wrong{MAX_LOGIN_ATTEMPTS + 1}"},
    )
    assert response.status_code == 403, response.text  # Forbidden


# Test READ
def test_read_user_requires_auth(client, registered_user):
    response = client.get(f"/spm/user/{registered_user['id']}")
    assert response.status_code == 401


def test_read_user_success(client, registered_user, user_token):
    response = client.get(
        f"/spm/user/{registered_user['id']}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200, response.text

    body = response.json()
    assert body["id"] == registered_user["id"]
    assert body["email"] == registered_user["email"]
    assert body["display_name"] == registered_user["display_name"]
    assert "created_at" in body


# Test UPDATE
def test_update_user_success(client, registered_user, user_token):
    updated_email = "updated@example.com"
    updated_password = "Newpass123%"
    updated_display_name = "Updated User"

    response = client.put(
        f"/spm/user/{registered_user['id']}",
        json={
            "email": updated_email,
            "password": updated_password,
            "display_name": updated_display_name,
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200, response.text

    body = response.json()
    assert body["email"] == updated_email
    assert body["display_name"] == updated_display_name


# Test DELETE
def test_delete_user_success(client, registered_user, user_token):
    # In the future, deleting a user will need to
    #   also delete the associated credentials from the table.
    #   UPDATE TEST
    response = client.delete(
        f"/spm/user/{registered_user['id']}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 204
