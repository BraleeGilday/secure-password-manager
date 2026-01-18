from datetime import datetime, timedelta, timezone
# from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
# from pwdlib import PasswordHash
from pydantic import BaseModel
from starlette.config import Config
from sqlalchemy import Session

from database import get_db

# From https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

# pwdlib for modern hashing; passlib for legacy hashing

config = Config(".env")
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/spm/user")


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


# "/spm/user/login" tuto="token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/spm/user/login")
app = FastAPI()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)
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
        token = Token(username=username)
    except InvalidTokenError:
        raise credentials_exception  
    
    # user = get_user(db=db, username=token.username)
    # if user is None:
    #     return credentials_exception
    # return user


# login for access token
@app.post("/login")
async def login_for_access_token(
    form_data:
    OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # user = get_user_by_username
    # if not user: raise HTTPException
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        # remove "" from user.username"
        data={"sub": "user.username"}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")