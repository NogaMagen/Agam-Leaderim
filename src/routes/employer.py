from fastapi import APIRouter, Depends

from schemas.create import EmployerCreate
from schemas.response import EmployerCreateResponse, EmployerSearchResponse
from security import get_current_user
from services.employer import EmployerService

router = APIRouter()
employee_service = EmployerService()


@router.post("/create", response_model=EmployerCreateResponse)
async def create_employee(employee: EmployerCreate, current_user: str = Depends(get_current_user)):
    return employee_service.create_employer(employee, current_user)


@router.get("/search", response_model=EmployerSearchResponse)
async def search_employees(filters: dict, current_user: str = Depends(get_current_user)):
    return employee_service.search_employers(filters, current_user)
