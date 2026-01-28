import pytest
import uuid


@pytest.fixture
def registered_user(client):
    """
    Creates a fresh user for the current test.
    Uses a unique email each time to avoid collisions with
    uniqueness constraints if anything leaks state.
    """
    suffix = uuid.uuid4().hex[:8]
    email = f"testuser_{suffix}@example.com"
    password = "testpassword"

    response = client.post(
        "/spm/user/register", json={"email": email, "password": password}
    )
    assert response.status_code == 200, response.text

    data = response.json()
    return {
        "id": data["id"],
        "email": data["email"],
        "username": data["username"],
        "password": password,  # plaintext for login
    }


@pytest.fixture
def user_token(client, registered_user):
    """
    Logs in as the registered user and returns a bearer token.
    """
    response = client.post(
        "/spm/user/login",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]
