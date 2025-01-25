from fastapi import APIRouter, Depends

from schemas.employee import EmployeeCreate, EmployeeAttachResponse , EmployeeCreateResponse, EmployeeSearchResponse
from security import get_current_user
from services.employee import EmployeeService

router = APIRouter()
employee_service = EmployeeService()


@router.post("/create", response_model=EmployeeCreateResponse,  operation_id="create_employee")
async def create_employee(employee: EmployeeCreate, current_user: str = Depends(get_current_user)):
    return employee_service.create_employee(employee, current_user)


@router.get("/search", response_model=EmployeeSearchResponse, operation_id="search_employer")
async def search_employees(search_term: str, page: int = 1, per_page: int = 10, current_user: str = Depends(get_current_user)):
    return employee_service.search_employees(search_term, page, per_page, current_user)


@router.post("/attach", response_model=EmployeeAttachResponse, operation_id="attach_employee_to_employer")
async def attach_employee_to_employer(attach_data: EmployeeAttach, current_user: str = Depends(get_current_user)):
    return employee_service.attach_employee_to_employer(attach_data, current_user)
