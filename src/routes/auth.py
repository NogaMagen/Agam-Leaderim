from fastapi import APIRouter

from schemas.create import UserCreate
from schemas.response import SignUpResponse, LoginResponse
from services.auth import Authservice

router = APIRouter()
auth_service = Authservice()


@router.post("/signup", response_model=SignUpResponse, operation_id="user_sign_up")
async def sign_up(user: UserCreate):
    return auth_service.sign_up(user)


@router.post("/login", response_model=LoginResponse)
async def log_in(user: UserCreate):
    return auth_service.log_in(user)
