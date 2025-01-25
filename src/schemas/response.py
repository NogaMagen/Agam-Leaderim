from typing import List

from pydantic import BaseModel

from schemas.create import UserCreate, EmployeeCreate, EmployerCreate


class SignUpResponse(BaseModel):
    message: str
    user: UserCreate | None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class EmployeeCreateResponse(BaseModel):
    message: str
    employee: EmployeeCreate


class EmployeeSearchResponse(BaseModel):
    employees: List[EmployeeCreate]


class EmployeeAttachResponse(BaseModel):
    message: str


class EmployerCreateResponse(BaseModel):
    message: str
    employee: EmployerCreate


class EmployerSearchResponse(BaseModel):
    employees: List[EmployerCreate]
