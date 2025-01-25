from typing import List, Optional

from pydantic import BaseModel


class EmployerCreate(BaseModel):
    name: str
    employees: str

    class Config:
        orm_mode = True


class EmployerCreateResponse(BaseModel):
    message: str
    employee: EmployerCreate


class EmployerSearchResponse(BaseModel):
    employees: List[EmployerCreate]


class EmployersSearch(BaseModel):
    search_term: str
    page: Optional[int] = 1
    per_page: Optional[int] = 10
