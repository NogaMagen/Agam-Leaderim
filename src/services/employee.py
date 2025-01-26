from fastapi.responses import JSONResponse

from data_layer.employee import EmployeeDataLayer
from schemas.employee import EmployeeCreate, EmployeeAttachCreate


class EmployeeService:
    def __init__(self):
        self._data_layer = EmployeeDataLayer()

    def create_employee(self, employee: EmployeeCreate, current_user: str = "j") -> JSONResponse:
        if not current_user:
            return JSONResponse(status_code=401, content="Unauthorized")

        new_employee = self._data_layer.create_employee(employee)
        return JSONResponse(content=f"Employee created successfully employee: {new_employee}",
                            status_code=201)

    def search_employees(self, search_term: str, current_user: str = "j") -> JSONResponse:

        if not current_user:
            return JSONResponse(status_code=401, content="Unauthorized")

        employees = self._data_layer.search_employee(search_term)
        return JSONResponse(content={"employees": employees}, status_code=200)

    def attach_employee_to_employer(self, attach_data: EmployeeAttachCreate, current_user: str = "j") -> JSONResponse:

        if not current_user:
            return JSONResponse(status_code=401, content="Unauthorized")

        success = self._data_layer.attach_employee_to_employer(attach_data)
        if success:
            return JSONResponse(content="Employee attached to employer successfully", status_code=200)
        else:
            return JSONResponse(
                content="Failed to attach employee (maybe already attached or invalid IDs)",
                status_code=400)
