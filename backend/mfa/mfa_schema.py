from pydantic import BaseModel

class TotpSetupResponse(BaseModel):
    issuer: str
    account_name: str
    otpauth_uri: str

class TotpConfirmRequest(BaseModel):
    code: str
    
class TotpCompleteRequest(BaseModel):
    mfa_token: str
    code: str