from cryptography.fernet import Fernet, InvalidToken
from starlette.config import Config

# Read environment variables / .env file
config = Config(".env")
CRED_ENC_KEY = config("CRED_ENC_KEY", default=None)

if CRED_ENC_KEY is None:
    raise RuntimeError("Missing CRED_ENC_KEY in .env")

# Create Fernet instance with env key (convert to bytes)
_fernet = Fernet(CRED_ENC_KEY.encode("utf-8"))


# -------------------- Encrypt / Decrypt Operations -------------------- #

def encrypt_password(plaintext: str) -> str:
    return _fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt_password(ciphertext: str) -> str:
    try:
        return _fernet.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
    except InvalidToken as e:
        raise ValueError("Invalid encrypted password / wrong key.") from e
