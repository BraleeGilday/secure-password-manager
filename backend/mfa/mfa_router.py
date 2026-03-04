from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from user.user_auth import get_current_user, decode_token, create_access_token
from user.user_crud import get_user_by_email

from mfa.mfa_schema import TotpSetupResponse, TotpConfirmRequest, TotpCompleteRequest

from mfa.mfa_service import (
    ISSUER_NAME,
    generate_totp_secret,
    build_provisioning_uri,
    verify_totp_code,
    current_totp_step,
)

from mfa.mfa_crud import set_totp_secret
from mfa.mfa_schema import TotpSetupResponse, TotpConfirmRequest

router = APIRouter(prefix="/spm/mfa", tags=["MFA"])

# TOTP is Time-based One-Time Password
@router.post("/totp/setup", response_model=TotpSetupResponse)
def totp_setup(
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    # 1) If already enabled, don't generate a new secret
    if user.totp_enabled:
        raise HTTPException(status_code=400, detail="TOTP already enabled.")

    # 2) Create a new secret and store it (but not enabled yet)
    secret = generate_totp_secret()
    set_totp_secret(db, user, secret)

    # 3) Create the URI the frontend will turn into a QR code
    uri = build_provisioning_uri(secret, user.email)

    return TotpSetupResponse(
        issuer=ISSUER_NAME,
        account_name=user.email,
        otpauth_uri=uri,
    )

@router.post("/totp/confirm")
def totp_confirm(
    body: TotpConfirmRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # basic sanity checks
    if not user.totp_secret:
        raise HTTPException(status_code=400, detail="TOTP not set up yet. Call /totp/setup first.")

    if user.totp_enabled:
        raise HTTPException(status_code=400, detail="TOTP already enabled.")

    # verify the code from Duo
    if not verify_totp_code(user.totp_secret, body.code, valid_window=1):
        raise HTTPException(status_code=400, detail="Invalid TOTP code.")

    step = current_totp_step()

    if user.totp_last_used_step is not None and step <= user.totp_last_used_step:
        raise HTTPException(status_code=400, detail="TOTP code already used.")

    # mark enabled + record last used step
    user.totp_enabled = True
    user.totp_last_used_step = step

    db.commit()
    db.refresh(user)

    return {"detail": "TOTP enabled", "user_email": user.email}


@router.post("/totp/complete")
def totp_complete(
    body: TotpCompleteRequest,
    db: Session = Depends(get_db),
):
    # 1) Validate the mfa_token (signature + expiry)
    payload = decode_token(body.mfa_token)

    # 2) Ensure this token is specifically for MFA completion
    if payload.get("mfa") is not True:
        raise HTTPException(status_code=401, detail="Invalid MFA token.")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid MFA token.")

    # 3) Load user
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid MFA token.")

    # 4) Must have MFA enabled + secret stored
    if not user.totp_enabled or not user.totp_secret:
        raise HTTPException(status_code=400, detail="MFA is not enabled for this user.")

    # 5) Verify the TOTP code
    if not verify_totp_code(user.totp_secret, body.code, valid_window=1):
        raise HTTPException(status_code=400, detail="Invalid TOTP code.")

    # 6) Replay protection (same style as confirm)
    step = current_totp_step()
    if user.totp_last_used_step is not None and step <= user.totp_last_used_step:
        raise HTTPException(status_code=400, detail="TOTP code already used.")

    user.totp_last_used_step = step
    db.commit()
    db.refresh(user)

    # 7) Issue the real bearer token
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer", "username": user.email}

@router.get("/totp/status")
def totp_status(user: User = Depends(get_current_user)):
    return {"totp_enabled": bool(user.totp_enabled)}
