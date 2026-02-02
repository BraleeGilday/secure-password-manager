from cryptography.fernet import Fernet, InvalidToken
from starlette.config import Config

# Read environment variables / .env file
config = Config(".env")

DEFAULT_TEST_CRED_ENC_KEY = "u36sOQjKvp93KNFIL4ACb3WJT-tV4Lp1qH8-XeWu0ko="  # valid Fernet key
CRED_ENC_KEY = config("CRED_ENC_KEY", default=DEFAULT_TEST_CRED_ENC_KEY)


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
