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
    get_user_by_username,
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

config = Config(".env")
router = APIRouter(prefix="/spm/user")

ACCESS_TOKEN_EXPIRE_MINUTES = int(config("TIMEOUT", default=1))


@router.post("/register")
def register_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    new_user = create_user(db=db, create_user=user_create)

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        # Not returning hashed password (unsafe)
    )


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    user = get_user_by_username(db, form_data.username)
    if not user or not password_hash.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer", username=user.username)


# Read "my user"
# GET /spm/{user_id}
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


# update "my_user"
# PATCH /spm/{user_id}
@router.patch("/{user_id}", response_model=UserResponse)
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

    updated = update_user(db=db, update_user=user_update, current_user=current_user)
    return updated


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
