from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def not_empty(cls, v: str) -> str: 
        if not v or not v.strip():
            raise ValueError("Required field!")
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @field_validator("password")
    def not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Required field!")
        return v


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    # Should we be returning password (even though it's hashed) in API responsse?

    class Config:
        from_attributes = True  # read attributes, not dicts


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
