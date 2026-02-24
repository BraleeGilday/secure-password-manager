from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: Optional[str] = None

    @field_validator("password")
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Required field!")
        return v


# Profile UPDATE (email or display name) without password
class UserProfileUpdate(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None

# Password UPDATE requires current password and new password
class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str

    @field_validator("current_password", "new_password")
    def password_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Required field!")
        return v

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    display_name: Optional[str] = None
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str  # email
