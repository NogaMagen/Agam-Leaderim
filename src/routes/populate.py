from fastapi import File, UploadFile, APIRouter
from fastapi.responses import JSONResponse

from services.populate import PopulateService

router = APIRouter()

populate = PopulateService()


@router.post("/populate/employees/", operation_id="populate_employers")
async def populate_employees(file: UploadFile = File(...)):
    await populate.populate_employees(file)
    return JSONResponse(status_code=200, content="Employees populated successfully")


@router.post("/populate/employers/", operation_id="populate_employees")
async def populate_employers(file: UploadFile = File(...)):
    await populate.populate_employers(file)
    return JSONResponse(status_code=200, content="Employers populated successfully")

:""