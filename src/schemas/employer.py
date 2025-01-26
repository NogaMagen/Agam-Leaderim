from typing import List

from pydantic import BaseModel


class EmployerCreate(BaseModel):
    name: str
    government_id: int

    class Config:
        orm_mode = True


class EmployerCreateResponse(BaseModel):
    message: str
    employer: EmployerCreate


class EmployerSearchResponse(BaseModel):
    employers: List[EmployerCreate]
