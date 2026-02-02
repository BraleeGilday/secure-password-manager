from typing import Optional
from pydantic import BaseModel, field_validator, ConfigDict


# -------------------- Request Models -------------------- #

class CredentialCreate(BaseModel):
    site: str
    username: str
    password: str
    notes: Optional[str] = None

    @field_validator('site', 'username', 'password')
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Required field cannot be empty!")
        return v


class CredentialUpdate(BaseModel):
    site: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    notes: Optional[str] = None

    @field_validator('site', 'username', 'password')
    def not_empty_if_provided(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v  # allow to not be provided
        if not v.strip():
            raise ValueError("Required field cannot be empty!")
        return v


# -------------------- Response Models -------------------- #

class CredentialOverviewOut(BaseModel):
    id: str
    site: str

    # Read as ORM object with attributes
    model_config = ConfigDict(from_attributes=True)


class CredentialEntryOut(BaseModel):
    id: str
    site: str
    username: str
    password: str
    notes: Optional[str] = None
    user_id: str

    # Read as ORM object with attributes instead of dict
    model_config = ConfigDict(from_attributes=True)
