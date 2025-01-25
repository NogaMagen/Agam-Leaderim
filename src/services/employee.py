from fastapi.responses import JSONResponse

from data_layer.employee import EmployeeDataLayer
from schemas.create import EmployeeCreate, EmployeeAttach


class EmployeeService:
    def __init__(self):
        self._data_layer = EmployeeDataLayer()

    def create_employee(self, employee: EmployeeCreate, current_user: str) -> JSONResponse:
        if not current_user:
            return JSONResponse(status_code=401, content="Unauthorized")

        new_employee = self._data_layer.create_employee(employee)
        return JSONResponse(content=f"Employee created successfully employee: {new_employee}",
                            status_code=201)

    def search_employees(self, search_term: str, page: int = 1, per_page: int = 10,
                         current_user: str = None) -> JSONResponse:
        if not current_user:
            return JSONResponse(status_code=401, content="Unauthorized")

        employees = self._data_layer.search_employee(search_term, page, per_page)
        return JSONResponse(content={"employees": employees}, status_code=200)

    def attach_employee_to_employer(self, attach_data: EmployeeAttach, current_user: str) -> JSONResponse:

        if not current_user:
            return JSONResponse(status_code=401, content="Unauthorized")

        success = self._data_layer.attach_employee_to_employer(
            employee_id=attach_data.employee_id,
            employer_id=attach_data.employer_id
        )
        if success:
            return JSONResponse(content="Employee attached to employer successfully", status_code=200)
        else:
            return JSONResponse(
                content="Failed to attach employee (maybe already attached or invalid IDs)",
                status_code=400)
