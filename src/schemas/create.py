from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    position: str
    government_id: str

    class Config:
        orm_mode = True


class EmployerCreate(BaseModel):
    name: str
    employees: str

    class Config:
        orm_mode = True


class EmployeeAttach(BaseModel):
    employee_id: int
    employer_id: int
