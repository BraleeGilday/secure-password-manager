from sqlalchemy.orm import Session  # for type hinting only

# Import both user and credential fixtures to register them with pytest
pytest_plugins = (
    "test_app.fixtures.user_fixtures",
    "test_app.fixtures.credential_fixtures",
)

from models import Credential
from credential.credential_crypto import decrypt_password


# Test CREATE credential (+ encryption/decryption)
def test_create_credential_encrypts_at_rest(created_credential, credential_payload, db: Session):
    # API returns the credential with plaintext password and correct field
    # (201 status code already asserted in credential_fixtures)
    assert created_credential["site"] == credential_payload["site"]
    assert created_credential["username"] == credential_payload["username"]
    assert created_credential["password"] == credential_payload["password"]
    assert created_credential["notes"] == credential_payload["notes"]
    cred_id = created_credential["id"]

    # Verify the password is stored as encrypted in the database (not plaintext)
    db_row = db.query(Credential).filter(Credential.id == cred_id).first()
    assert db_row is not None
    assert db_row.password != credential_payload["password"]

    # Ensure the stored password can be decrypted back to the original
    assert decrypt_password(str(db_row.password)) == credential_payload["password"]


# Test READ ALL credentials
def test_list_credentials_returns_overview(client, auth_headers, created_credential):
    response = client.get("/spm/credentials", headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)

    # List should include the created credential, but only id and site fields (no sensitive data)
    matches = [item for item in data if item["id"] == created_credential["id"]]
    assert matches, "Created credential not found in list response"
    assert set(matches[0].keys()) == {"id", "site"}


# Test READ credential (one)
def test_read_credential_by_id(client, auth_headers, created_credential):
    cred_id = created_credential["id"]
    response = client.get(f"/spm/credentials/{cred_id}", headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == cred_id

    # Endpoint should return the password in plaintext (+ other fields)
    assert data["password"] == created_credential["password"]
    assert data["site"] == created_credential["site"]
    assert data["username"] == created_credential["username"]
    assert data["notes"] == created_credential["notes"]


# Test UPDATE credential
def test_update_credential_by_id(client, auth_headers, created_credential, db: Session):
    cred_id = created_credential["id"]
    new_password = "my_updated_password_456!"
    new_notes = "updated by pytest"
    # Send partial update
    response = client.patch(
        f"/spm/credentials/{cred_id}",
        json={"password": new_password, "notes": new_notes},
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == cred_id
    assert data["password"] == new_password
    assert data["notes"] == new_notes

    # The updated password should be stored encrypted in the database
    db_row = db.query(Credential).filter(Credential.id == cred_id).first()
    assert db_row is not None
    assert db_row.password != new_password
    assert decrypt_password(str(db_row.password)) == new_password


# Test DELETE credential
def test_delete_credential_by_id(client, auth_headers, created_credential):
    cred_id = created_credential["id"]
    response = client.delete(f"/spm/credentials/{cred_id}", headers=auth_headers)
    assert response.status_code == 204, response.text

    # After deletion, reading the credential should return 404 not found
    response = client.get(f"/spm/credentials/{cred_id}", headers=auth_headers)
    assert response.status_code == 404
