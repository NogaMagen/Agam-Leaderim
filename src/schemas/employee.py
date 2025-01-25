from typing import List, Optional

from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    position: str
    government_id: str

    class Config:
        orm_mode = True


class EmployeesSearch(BaseModel):
    search_term: str
    page: Optional[int] = 1
    per_page: Optional[int] = 10


class EmployeeAttach(BaseModel):
    employee_id: int
    employer_id: int


class EmployeeCreateResponse(BaseModel):
    message: str
    employee: EmployeeCreate


class EmployeeSearchResponse(BaseModel):
    employees: List[EmployeeCreate]


class EmployeeAttachResponse(BaseModel):
    message: str
