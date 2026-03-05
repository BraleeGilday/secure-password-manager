from sqlalchemy.orm import Session
from models import User


def set_totp_secret(db: Session, user: User, secret: str) -> User:
    """
    Store a new TOTP secret for the user.
    Does NOT enable TOTP yet.
    """
    user.totp_secret = secret
    user.totp_enabled = False
    user.totp_last_used_step = None

    db.commit()
    db.refresh(user)
    return user


def enable_totp(db: Session, user: User) -> User:
    """
    Mark TOTP as enabled (assumes code was already verified).
    """
    user.totp_enabled = True
    db.commit()
    db.refresh(user)
    return user