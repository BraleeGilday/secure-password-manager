from fastapi import APIRouter
from pwd_generator.pwd_schema import (
    PasswordRequest,
    PasswordResponse,
)
from pwd_generator.pwd_generator import (
    generate_password,
)

router = APIRouter(prefix="/spm/password")


@router.post("/generate", response_model=PasswordResponse)
async def create_password(request: PasswordRequest) -> PasswordResponse:
    pwd = generate_password(
        length=request.length,
        has_symbols=request.has_symbols,
        has_numbers=request.has_numbers,
        mixed_case=request.mixed_case,
        )
    # evaluate strength?
    return PasswordResponse(password=pwd)
