from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from user.user_auth import get_current_user
from models import User

from mfa.mfa_service import ISSUER_NAME, generate_totp_secret, build_provisioning_uri
from mfa.mfa_crud import set_totp_secret
from mfa.mfa_schema import TotpSetupResponse

router = APIRouter(prefix="/spm//mfa", tags=["MFA"])

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
def totp_confirm(user=Depends(get_current_user)):
    
    return {"message": "confirm endpoint reached", "user_email": user.email}