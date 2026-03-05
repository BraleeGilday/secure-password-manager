from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from user.user_auth import get_current_user, create_access_token, get_user_from_mfa_token

from mfa.mfa_schema import (
    TotpSetupRequest,
    TotpSetupResponse,
    TotpCompleteRequest,
    TotpEnrollmentStatusRequest,
)

from mfa.mfa_service import (
    ISSUER_NAME,
    generate_totp_secret,
    build_provisioning_uri,
    verify_totp_code,
    current_totp_step,
)

from mfa.mfa_crud import set_totp_secret

router = APIRouter(prefix="/spm/mfa", tags=["MFA"])


def _replay_protect_or_400(user: User) -> int:
    """
    Returns current step if it's usable; otherwise raises.
    """
    step = current_totp_step()
    if user.totp_last_used_step is not None and step <= user.totp_last_used_step:
        raise HTTPException(status_code=400, detail="TOTP code already used.")
    return step


@router.post("/totp/setup", response_model=TotpSetupResponse)
def totp_setup(
    body: TotpSetupRequest,
    db: Session = Depends(get_db),
):
    """
    Start enrollment: generate and store a new secret, return otpauth URI.
    Uses mfa_token (not access token).
    """
    user = get_user_from_mfa_token(body.mfa_token, db)

    if user.totp_enabled:
        raise HTTPException(status_code=400, detail="TOTP already enabled.")

    secret = generate_totp_secret()
    set_totp_secret(db, user, secret)

    uri = build_provisioning_uri(secret, user.email)

    return TotpSetupResponse(
        issuer=ISSUER_NAME,
        account_name=user.email,
        otpauth_uri=uri,
    )


@router.post("/totp/complete")
def totp_complete(
    body: TotpCompleteRequest,
    db: Session = Depends(get_db),
):
    """
    Finish enrollment: verify code, enable MFA, and issue a real access token.
    Uses mfa_token (not access token).
    """
    user = get_user_from_mfa_token(body.mfa_token, db)

    if not user.totp_secret:
        raise HTTPException(status_code=400, detail="TOTP not set up yet. Call /totp/setup first.")

    if not verify_totp_code(user.totp_secret, body.code, valid_window=1):
        raise HTTPException(status_code=400, detail="Invalid TOTP code.")

    step = _replay_protect_or_400(user)

    user.totp_enabled = True
    user.totp_last_used_step = step
    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "username": user.email}


@router.post("/totp/verify")
def totp_verify(
    body: TotpCompleteRequest,
    db: Session = Depends(get_db),
):
    """
    Verify on login: requires already-enrolled MFA; verifies code; issues access token.
    Uses mfa_token (not access token).
    """
    user = get_user_from_mfa_token(body.mfa_token, db)

    if not user.totp_enabled or not user.totp_secret:
        # Keep this string stable if the frontend branches on it
        raise HTTPException(status_code=400, detail="MFA not enrolled")

    if not verify_totp_code(user.totp_secret, body.code, valid_window=1):
        raise HTTPException(status_code=400, detail="Invalid TOTP code.")

    step = _replay_protect_or_400(user)

    user.totp_last_used_step = step
    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "username": user.email}


@router.get("/totp/status")
def totp_status(user: User = Depends(get_current_user)):
    """
    Status for logged-in users (access-token protected).
    """
    return {"totp_enabled": bool(user.totp_enabled)}


@router.post("/totp/enrollment-status")
def totp_enrollment_status(
    body: TotpEnrollmentStatusRequest,
    db: Session = Depends(get_db),
):
    """
    Helper: lets you decide setup vs verify using mfa_token.
    """
    user = get_user_from_mfa_token(body.mfa_token, db)
    return {"totp_enabled": bool(user.totp_enabled), "has_secret": bool(user.totp_secret)}
