import uuid
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from models import User, Credential
from user.user_schema import UserCreate, UserProfileUpdate, UserPasswordUpdate

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
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user_profile(db: Session, update_profile: UserProfileUpdate, current_user: User) -> User:
    """
    update user (email and display name)
    """
    user = get_user_by_id(db, current_user.id)

    user.email = update_profile.email
    user.display_name = update_profile.display_name

    db.commit()
    db.refresh(user)
    return user


def update_user_password(db: Session, update_password: UserPasswordUpdate, current_user: User) -> User:
    """
    update user password (only)
    """
    user = get_user_by_id(db, current_user.id)

    # Verify current password matches stored hash
    if not password_hash.verify(update_password.current_password, user.password):
        raise ValueError("Incorrect password")

    user.password = password_hash.hash(update_password.new_password)

    db.commit()
    db.refresh(user)
    return user

"""
OLD ONE HERE

def delete_user(db: Session, current_user: User) -> None:
    
    remove user

    **TO-DO: UPDATE**
    When a user is deleted, their associated credentials also need to get deleted.
    (In credential, FK- user.id, on delete CASCADE)
    
    
    db.delete(current_user)
    db.commit()
"""

# NEW ONE: DELETES ALL CREDENTIALS BEFORE DELETING USER (tried delete cascade on models but SQLite didnt like it, may need other changes if using cascade. tbd)
def delete_user(db: Session, current_user: User) -> None:
    """
    Delete user and ALL their credentials first,
    uses bulk deletes to avoid setting credential.user_id = NULL.
    """

    # 1) Delete credentials owned by the user
    db.query(Credential).filter(Credential.user_id == current_user.id).delete(
        synchronize_session=False
    )

    # 2) Delete the user
    db.query(User).filter(User.id == current_user.id).delete(
        synchronize_session=False
    )

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


def increment_login_attempts(db: Session, user: User) -> None:
    user.login_attempts += 1
    db.commit()
    db.refresh(user)
    return


def reset_login_attempts(db: Session, user: User) -> None:
    user.login_attempts = 0
    db.commit()
    db.refresh(user)
    return
