from typing import List

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
