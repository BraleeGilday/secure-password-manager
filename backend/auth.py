from datetime import datetime, timedelta, timezone
import jwt
from starlette.config import Config

config = Config(".env")
SECRET_KEY = config("SECRET_KEY")

ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
