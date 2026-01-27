import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
from starlette.config import Config
from sqlalchemy.orm import Session

from user.user_crud import get_user_by_username

from database import get_db

config = Config(".env")
SECRET_KEY = config("SECRET_KEY", default="SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("TIMEOUT", default=1))

router = APIRouter(prefix="/spm/user")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/spm/user/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        # token = Token(username=username)
    except PyJWTError:
        raise credentials_exception

    user = get_user_by_username(db=db, username=username)
    if user is None:
        raise credentials_exception
    return user
