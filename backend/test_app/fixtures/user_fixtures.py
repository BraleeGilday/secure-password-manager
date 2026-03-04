import pytest
import uuid
import pyotp
from urllib.parse import urlparse, parse_qs


@pytest.fixture
def registered_user(client):
    """
    Creates a fresh user for the current test.
    Uses a unique email each time to avoid collisions with
    uniqueness constraints if anything leaks state.
    """
    suffix = uuid.uuid4().hex[:8]
    email = f"testuser_{suffix}@example.com"
    password = "testpassword123!"
    # no display_name, so email prefix should be used by default

    response = client.post(
        "/spm/user/register", json={"email": email, "password": password}
    )
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["display_name"] == email.split("@")[0]

    return {
        "id": data["id"],
        "email": data["email"],
        "display_name": data["display_name"],
        "password": password,  # plaintext for login
    }


@pytest.fixture
def user_token(client, registered_user):
    """
    Full auth flow:
      1) login -> mfa_token
      2) totp/setup -> otpauth_uri (contains secret)
      3) generate TOTP code
      4) totp/complete -> access_token
    Returns bearer access_token.
    """
    # 1) Login (returns MFA challenge)
    login = client.post(
        "/spm/user/login",
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert login.status_code == 200, login.text
    login_body = login.json()
    assert login_body.get("mfa_required") is True, login_body
    mfa_token = login_body["mfa_token"]

    # 2) Start TOTP setup (returns otpauth_uri)
    setup = client.post("/spm/mfa/totp/setup", json={"mfa_token": mfa_token})
    assert setup.status_code == 200, setup.text
    otpauth_uri = setup.json()["otpauth_uri"]

    # 3) Parse secret from otpauth_uri and generate a valid code
    # otpauth://totp/...?...&secret=BASE32&issuer=...
    parsed = urlparse(otpauth_uri)
    qs = parse_qs(parsed.query)
    secret = qs["secret"][0]
    code = pyotp.TOTP(secret).now()

    # 4) Complete enrollment -> get real access token
    complete = client.post(
        "/spm/mfa/totp/complete",
        json={"mfa_token": mfa_token, "code": code},
    )
    assert complete.status_code == 200, complete.text
    return complete.json()["access_token"]