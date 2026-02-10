from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from user.user_auth import get_current_user
from models import User, Credential

from credential.credential_crud import (
    get_credential_for_user,
    search_credentials_for_user,  # handles get_all_credentials_user too
    create_credential,
    update_credential,
    delete_credential
)

from credential.credential_schema import (
    CredentialCreate,
    CredentialUpdate,
    CredentialOverviewOut,
    CredentialEntryOut,
)

from credential.credential_crypto import decrypt_password


# Initialize router
router = APIRouter(prefix="/spm/credentials")


# -------------------- Decryption Helper -------------------- #

def _to_entry_out(cred: Credential) -> CredentialEntryOut:
    try:
        plain_pw = decrypt_password(cred.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stored password could not be decrypted",
        )

    return CredentialEntryOut(
        id=cred.id,
        site=cred.site,
        username=cred.username,
        password=plain_pw,
        notes=cred.notes,
        user_id=cred.user_id,
    )


# -------------------- Router Endpoints -------------------- #

# Create a credential entry
@router.post("/", response_model=CredentialEntryOut, status_code=status.HTTP_201_CREATED)
def create_credential_route(
    credential_create: CredentialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CredentialEntryOut:

    cred = create_credential(db=db, create_credential=credential_create, current_user=current_user)
    return _to_entry_out(cred)


# Read all credentials in overview (can search by site)
@router.get("/", response_model=list[CredentialOverviewOut])
def list_credentials_route(
    search: str | None = Query(default=None, description="Search by site"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CredentialOverviewOut]:

    # Defaults to get_all_credentials_for_user if no search
    creds = search_credentials_for_user(db=db, user_id=current_user.id, search=search)
    return creds


# Read one credential entry
@router.get("/{credential_id}", response_model=CredentialEntryOut)
def read_credential_route(
    credential_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CredentialEntryOut:

    cred = get_credential_for_user(db=db, credential_id=credential_id, user_id=current_user.id)
    if cred is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")
    return _to_entry_out(cred)


# Update an existing credential entry
@router.patch("/{credential_id}", response_model=CredentialEntryOut)
def update_credential_route(
    credential_id: str,
    credential_update: CredentialUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CredentialEntryOut:

    updated = update_credential(
        db=db,
        credential_id=credential_id,
        update_credential=credential_update,
        current_user=current_user,
    )
    return _to_entry_out(updated)


# Delete a credential entry
@router.delete("/{credential_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_credential_route(
    credential_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    delete_credential(db=db, credential_id=credential_id, current_user=current_user)
    return None
