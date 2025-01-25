from fastapi import APIRouter, Depends

from schemas.employee import EmployeeCreate, EmployeeAttachResponse, EmployeeCreateResponse, EmployeeSearchResponse, \
    EmployeeAttach
from security import get_current_user
from services.employee import EmployeeService

router = APIRouter()
employee_service = EmployeeService()


@router.post("/attach", response_model=EmployeeAttachResponse, operation_id="attach_employee_to_employee")
async def attach_employee_to_employer(attach_data: EmployeeAttach, current_user: str = Depends(get_current_user)):
    return employee_service.attach_employee_to_employer(attach_data, current_user)


@router.post("/create_employee", response_model=EmployeeCreateResponse, operation_id="create_employee")
async def create_employee(employee: EmployeeCreate, current_user: str = Depends(get_current_user)):
    return employee_service.create_employee(employee, current_user)


@router.get("/search_employees", response_model=EmployeeSearchResponse, operation_id="search_employees")
async def search_employees(search_term: str,
                           current_user: str = Depends(get_current_user)):
    return employee_service.search_employees(search_term, current_user)
