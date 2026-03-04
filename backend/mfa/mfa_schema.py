from pydantic import BaseModel

class TotpSetupRequest(BaseModel):
    mfa_token: str

class TotpSetupResponse(BaseModel):
    issuer: str
    account_name: str
    otpauth_uri: str

class TotpConfirmRequest(BaseModel):
    mfa_token: str
    code: str

class TotpCompleteRequest(BaseModel):
    mfa_token: str
    code: str

class TotpEnrollmentStatusRequest(BaseModel):
    mfa_token: str