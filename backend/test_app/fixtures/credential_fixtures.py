import pytest
import uuid


@pytest.fixture
def auth_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def credential_payload():
    """
    Generates a unique credential payload for current test.
    """
    suffix = uuid.uuid4().hex[:8]  # randomize
    return {
        "site": f"https://example.com/{suffix}",
        "username": f"creduser_{suffix}",
        "password": "my_test_password_123!",
        "notes": "created by pytest",
    }


@pytest.fixture
def created_credential(client, auth_headers, credential_payload):
    """
    Creates a credential via the API and returns its JSON response.
    """
    response = client.post(
        "/spm/credentials/",
        json=credential_payload,
        headers=auth_headers,
    )
    assert response.status_code == 201, response.text
    return response.json()
