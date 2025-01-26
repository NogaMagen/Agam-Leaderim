from typing import List

from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    id: int
    first_name: str
    last_name: str
    position: str
    government_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class EmployeeAttachCreate(BaseModel):
    employee_id: int
    employer_id: int


class EmployeeCreateResponse(BaseModel):
    message: str
    employee: EmployeeCreate


class EmployeeSearchResponse(BaseModel):
    employees: List[EmployeeCreate]


class EmployeeAttachResponse(BaseModel):
    message: str
