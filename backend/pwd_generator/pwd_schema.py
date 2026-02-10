from pydantic import BaseModel, Field


class PasswordRequest(BaseModel):
    length: int = Field(default=16, ge=8, le=64)
    has_symbols: bool = Field(default=True)
    has_numbers: bool = Field(default=True)
    mixed_case: bool = Field(default=True)


class PasswordResponse(BaseModel):
    password: str
    # strength: str
