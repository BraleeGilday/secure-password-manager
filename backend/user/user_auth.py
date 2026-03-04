import jwt
from jwt.exceptions import PyJWTError

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from datetime import datetime, timedelta, timezone

from config import get_settings
from database import get_db
from user.user_crud import get_user_by_email

# config = Config(".env")

# SECRET_KEY = config("SECRET_KEY", default="dev-secret-key-change-me")
# ALGORITHM = "HS256"

settings = get_settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

router = APIRouter(prefix="/spm/user")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/spm/user/login")


# ------------ Token creation ------------
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---- dependency: get current user from token ----
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
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        # Don't allow MFA tokens to act as access tokens
        if payload.get("mfa") is True:
            raise credentials_exception

    except PyJWTError:
        raise credentials_exception

    user = get_user_by_email(db=db, email=email)
    if user is None:
        raise credentials_exception
    return user


def create_mfa_token(email: str) -> str:
    """
    Short-lived token used ONLY to complete MFA.
    """
    return create_access_token(
        data={"sub": email, "mfa": True},
        expires_delta=timedelta(minutes=5),
    )


def decode_token(token: str) -> dict:
    """
    Decode a JWT and return its payload (or raise HTTPException).
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

def get_user_from_mfa_token(
    mfa_token: str,
    db: Session,
):
    payload = decode_token(mfa_token)

    if payload.get("mfa") is not True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid MFA token.")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid MFA token.")

    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid MFA token.")

    return user