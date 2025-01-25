from fastapi import APIRouter

from schemas.auth import UserCreate
from schemas.auth import SignUpResponse, LoginResponse
from services.auth import Authservice

router = APIRouter()
auth_service = Authservice()


@router.post("/signup", response_model=SignUpResponse, operation_id="signup")
async def sign_up(user: UserCreate):
    return auth_service.sign_up(user)


@router.post("/login", response_model=LoginResponse, operation_id="login")
async def log_in(user: UserCreate):
    return auth_service.log_in(user)
