from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
)
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from starlette import status
from starlette.config import Config
from datetime import timedelta

from database import get_db
from user.user_crud import (
    create_user,
    update_user,
    delete_user,
    get_user_by_id,
    get_user_by_email,
    password_hash,
)
from user.user_auth import get_current_user

from user.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse,
    Token,
)

from models import (
    User,
)

from auth import (
    create_access_token,
)

router = APIRouter(prefix="/spm/user")
config = Config(".env")

ACCESS_TOKEN_EXPIRE_MINUTES = int(config("TIMEOUT", default=1))
MAX_LOGIN_ATTEMPTS = 4


# CREATE
@router.post("/register")
def register_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    new_user = create_user(db=db, create_user=user_create)

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        display_name=new_user.display_name,
        created_at=new_user.created_at,
    )


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    user = get_user_by_email(
        db, form_data.username
    )  # for a user, email *is* the username
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Too many failed attempts
    if user.login_attempts >= MAX_LOGIN_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            headers={"WWW-Authenticate": "Bearer"},
            detail="Account locked. Too many failed login attempts.",
        )

    # Incorrect password
    if not password_hash.verify(form_data.password, user.password):
        user.login_attempts += 1
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Correct password
    user.login_attempts = 0
    db.commit()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer", username=user.email)


# READ
@router.get("/{user_id}", response_model=UserResponse)
def read_user_route(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


# UPDATE
@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    updated = update_user(
        db=db,
        update_user=user_update,
        current_user=current_user,
    )
    return updated


# DELETE
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )

    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    delete_user(db, user)
    return None
