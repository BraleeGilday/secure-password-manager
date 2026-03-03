from pydantic import BaseModel

class TotpSetupResponse(BaseModel):
    issuer: str
    account_name: str
    otpauth_uri: str