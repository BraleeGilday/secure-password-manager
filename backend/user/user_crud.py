import uuid
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from models import User
from user.user_schema import UserCreate, UserUpdate

password_hash = PasswordHash.recommended()  # may be replaced


def generate_unique_username(db: Session, email: str) -> str:
    username_base = email.split("@", 1)[0]
    username_candidate = username_base

    n = 1
    while db.query(User).filter(User.username == username_candidate).first():
        n += 1
        username_candidate = f"{username_base}{n}"
    return username_candidate


def create_user(db: Session, create_user: UserCreate) -> User:
    """
    create new user
    """
    new_user = User(
        id=str(uuid.uuid4()),
        email=create_user.email,
        username=generate_unique_username(db, create_user.email),
        password=password_hash.hash(create_user.password),
    )
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already registered",
        )

    db.refresh(new_user)
    return new_user


def update_user(db: Session, update_user: UserUpdate, current_user: User) -> User:
    """
    update user (email and/or password only)
    """
    user = get_user_by_id(db, current_user.id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if update_user.email is not None:
        user.email = update_user.email

    if update_user.password is not None:
        user.password = password_hash.hash(update_user.password)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already registered",
        )

    db.refresh(user)
    return user


def delete_user(db: Session, current_user: User) -> None:
    """
    remove user
    """
    db.delete(current_user)
    db.commit()


#  - - - - - - - - - -
#   UTILITIES
#  - - - - - - - - - -


def get_user_by_id(db: Session, user_id: str) -> User | None:
    """
    Retrieve user by id
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Retrieve user by username
    """
    return db.query(User).filter(User.username == username).first()


def get_all_users(db: Session):
    return db.query(User).all()
