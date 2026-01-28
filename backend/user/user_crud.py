import uuid
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from models import User
from user.user_schema import UserCreate, UserUpdate

password_hash = PasswordHash.recommended()  # may be replaced


def create_user(db: Session, create_user: UserCreate) -> User:
    """
    create new user
    """
    name = create_user.display_name
    if name is None or not name.strip():
        name = create_user.email.split("@", 1)[0]

    new_user = User(
        id=str(uuid.uuid4()),
        email=create_user.email,
        password=password_hash.hash(create_user.password),
        display_name=name,
        login_attempts=0,
    )
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    db.refresh(new_user)
    return new_user


def update_user(db: Session, update_user: UserUpdate, current_user: User) -> User:
    """
    update user (email, password, and display name)
    """
    user = get_user_by_id(db, current_user.id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user.email = update_user.email
    user.password = password_hash.hash(update_user.password)
    user.display_name = update_user.display_name

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    db.refresh(user)
    return user


def delete_user(db: Session, current_user: User) -> None:
    """
    remove user

    **TO-DO: UPDATE**
    When a user is deleted, their associated credentials also need to get deleted.
    (In credential, FK- user.id, on delete CASCADE)
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


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Retrieve user by email
    """
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session):
    return db.query(User).all()
