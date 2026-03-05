import pyotp
import time

# The "app name" shown in the authenticator
ISSUER_NAME = "Secure Password Manager"

def generate_totp_secret() -> str:
    """
    Generate a new Base32 secret for a user's authenticator app.
    """
    return pyotp.random_base32()


def build_provisioning_uri(secret: str, user_email: str) -> str:
    """
    Creates the QR code link (i.e., otpauth:// URI) for the authenticator app.

    Note:
    The provisioning URI is what becomes the QR code. Duo scans it and stores the secret.
    """
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=user_email, issuer_name=ISSUER_NAME)


def verify_totp_code(secret: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify a 6-digit TOTP code. valid_window=1 allows +/- one 30-second step
    (helps if the server and phone clocks are slightly out of sync).
    """
    cleaned = "".join(code.split())     # handle pasted "123 456"
    totp = pyotp.TOTP(secret)
    return bool(totp.verify(cleaned, valid_window=valid_window))

def current_totp_step() -> int:
    """
    Returns the current TOTP time step (30-second window).
    """
    return int(time.time()) // 30