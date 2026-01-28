from test_app.fixtures.user_fixtures import registered_user, user_token

import uuid


def test_register_user(client):
    suffix = uuid.uuid4().hex[:8]

    email = f"user_{suffix}@example.com"

    response = client.post(
        "/spm/user/register",
        json={
            "email": email,
            "password": "password123",
        },
    )
    assert response.status_code == 200, response.text

    body = response.json()
    assert "id" in body
    assert "username" in body
    assert body["email"] == email


def test_login_user_gets_token(client, registered_user):
    response = client.post(
        "/spm/user/login",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200, response.text

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


def test_read_user_success(client, registered_user, user_token):
    response = client.get(
        f"/spm/user/{registered_user['id']}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200, response.text

    body = response.json()
    assert body["id"] == registered_user["id"]
    assert body["email"] == registered_user["email"]
    assert body["username"] == registered_user["username"]


def test_update_user_success(client, registered_user, user_token):
    updated_email = "updated@example.com"
    response = client.patch(
        f"/spm/user/{registered_user['id']}",
        json={"email": updated_email},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["email"] == updated_email


def test_delete_user_success(client, registered_user, user_token):
    # In the future, deleting a user will need to
    #   also delete the associated credentials from the table.
    #   UPDATE TEST
    response = client.delete(
        f"/spm/user/{registered_user['id']}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 204
