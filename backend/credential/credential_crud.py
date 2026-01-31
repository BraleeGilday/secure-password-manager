from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Credential, User
from credential.credential_schema import CredentialCreate, CredentialUpdate

from credential.credential_crypto import encrypt_password


# -------------------- Utilities -------------------- #

def get_credential_for_user(db: Session, credential_id: str, user_id: str) -> Credential | None:
    """
    Retrieve credential for a specific user by id (with ownership check).
    """
    return db.query(Credential).filter(Credential.id == credential_id, Credential.user_id == user_id).first()


def get_all_credentials_for_user(db: Session, user_id: str, search: str | None = None):
    """
    Retrieve all credentials owned by a user (vault overview list).
    Optional search to filter results by site.
    """
    q = db.query(Credential).filter(Credential.user_id == user_id)

    if search:
        s = search.strip()
        if s:
            pattern = f"%{s}%"
            q = q.filter(Credential.site.ilike(pattern))

    return q.order_by(Credential.site.asc()).all()


# -------------------- CRUD Operations -------------------- #

def create_credential(
        db: Session,
        create_credential: CredentialCreate,
        current_user: User
) -> Credential:
    """
    Create a new credential owned by current_user.
    """
    new_cred = Credential(
        site=create_credential.site,
        username=create_credential.username,
        password=encrypt_password(create_credential.password),
        notes=create_credential.notes,
        user_id=current_user.id,
    )

    db.add(new_cred)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Could not create credential due to a database constraint",
        )

    db.refresh(new_cred)
    return new_cred


def update_credential(
    db: Session,
    credential_id: str,
    update_credential: CredentialUpdate,
    current_user: User,
) -> Credential:
    """
    Update an existing credential owned by current_user (only fields that are not None are updated).
    """
    cred = get_credential_for_user(db, credential_id, current_user.id)
    if cred is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")

    if update_credential.site is not None:
        cred.site = update_credential.site
    if update_credential.username is not None:
        cred.username = update_credential.username
    if update_credential.password is not None:
        cred.password = encrypt_password(update_credential.password)
    if update_credential.notes is not None:
        cred.notes = update_credential.notes

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Could not update credential due to a database constraint",
        )

    db.refresh(cred)
    return cred


def delete_credential(
        db: Session,
        credential_id: str,
        current_user: User
) -> None:
    """
    Delete a credential owned by current_user.
    """
    cred = get_credential_for_user(db, credential_id, current_user.id)
    if cred is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")

    db.delete(cred)
    db.commit()
