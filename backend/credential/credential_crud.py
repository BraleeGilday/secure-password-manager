from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Credential, User
from credential.credential_schema import CredentialCreate, CredentialUpdate
from credential.credential_crypto import encrypt_password


# -------------------- Utilities -------------------- #

def get_credential_for_user(db: Session, credential_id: str, user_id: str) -> Credential | None:
    """
    Retrieve credential by id, then verify it belongs to user_id.
    """
    # Verify user owns the credential being accessed
    cred = db.query(Credential).filter(Credential.id == credential_id).first()
    if cred is None or cred.user_id != user_id:
        return None
    return cred


def get_all_credentials_for_user(db: Session, user_id: str):
    """
    Retrieve all credentials owned by a user (vault overview list).
    """
    q = (
        db.query(Credential)
        .filter(Credential.user_id == user_id)
        .order_by(Credential.site.asc())
    )
    return q.all()  # type = list[Credential]


def search_credentials_for_user(db: Session, user_id: str, search: str | None = None):
    """
    Search by site to filter for credentials owned by a user (vault overview list).
    """
    s = (search or "").strip()
    if not s:
        return get_all_credentials_for_user(db, user_id)

    pattern = f"%{s}%"
    q = (
        db.query(Credential)
        .filter(Credential.user_id == user_id, Credential.site.ilike(pattern))
        .order_by(Credential.site.asc())
    )
    return q.all()  # type = list[Credential]


def _site_username_in_use(db: Session, *, user_id: str, site: str, username: str, exclude_credential_id: str | None = None,
) -> bool:
    """
    Returns True if another credential exists for user with the same site and username, False otherwise.
    This helper is for checking if a credential can be created/updated without duplicating a username for the same site.
    """
    q = (
        db.query(Credential)
        .filter(
            Credential.user_id == user_id,
            Credential.site == site,
            Credential.username == username,
        )
    )
    if exclude_credential_id is not None:
        q = q.filter(Credential.id != exclude_credential_id)
    return q.first() is not None


# -------------------- CRUD Operations -------------------- #

def create_credential(
        db: Session,
        create_credential: CredentialCreate,
        current_user: User
) -> Credential:
    """
    Create a new credential owned by current_user.
    """
    # Check if valid authenticated user
    if not current_user or not current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

    # Pre-check duplicate username/site combo before altering database
    if _site_username_in_use(
        db,
        user_id=current_user.id,
        site=create_credential.site,
        username=create_credential.username,
    ):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A credential for this site and username already exists")

    new_cred = Credential(
        site=create_credential.site,
        username=create_credential.username,
        password=encrypt_password(create_credential.password),
        notes=create_credential.notes,
        user_id=current_user.id,
    )

    db.add(new_cred)
    # Check if unexpected constraint in database (kept for safety, but the above filter checks for duplicate username/site already)
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
    # Check if valid authenticated user
    if not current_user or not current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

    # Check if credential exists and curr_user owns it
    cred = get_credential_for_user(db, credential_id, current_user.id)
    if cred is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")

    # Only check uniqueness if site/username might change
    if update_credential.site is not None or update_credential.username is not None:
        new_site = update_credential.site if update_credential.site is not None else cred.site
        new_username = update_credential.username if update_credential.username is not None else cred.username

        if _site_username_in_use(
            db,
            user_id=current_user.id,
            site=new_site,
            username=new_username,
            exclude_credential_id=cred.id,
        ):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A credential for this site and username already exists")

    if update_credential.site is not None:
        cred.site = update_credential.site
    if update_credential.username is not None:
        cred.username = update_credential.username
    if update_credential.password is not None:
        cred.password = encrypt_password(update_credential.password)
    if update_credential.notes is not None:
        cred.notes = update_credential.notes

    # Check if unexpected constraint in database (kept for safety, but the above filter checks for duplicate username/site already)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not update credential due to a database constraint")

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
    # Check if valid authenticated user
    if not current_user or not current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

    # Check if credential exists and curr_user owns it
    cred = get_credential_for_user(db, credential_id, current_user.id)
    if cred is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")

    db.delete(cred)
    db.commit()
