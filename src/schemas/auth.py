from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class SignUpResponse(BaseModel):
    message: str
    user: UserCreate | None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
