from fastapi import APIRouter, Depends

from schemas.employer import EmployerCreate, EmployerCreateResponse, EmployerSearchResponse
from security import get_current_user
from services.employer import EmployerService

router = APIRouter()
employer_service = EmployerService()


@router.post("/create_employer", response_model=EmployerCreateResponse, operation_id="create_employer")
async def create_employer(employer: EmployerCreate, current_user: str = Depends(get_current_user)):
    return employer_service.create_employer(employer, current_user)


@router.get("/search_employers", response_model=EmployerSearchResponse, operation_id="search_employers")
async def search_employers(search_term: str,
                           current_user: str = Depends(get_current_user)):
    return employer_service.search_employers(search_term, current_user)
