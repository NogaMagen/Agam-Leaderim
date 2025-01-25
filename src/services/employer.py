from fastapi.responses import JSONResponse

from data_layer.employer import EmployerDataLayer
from schemas.employer import EmployerCreate, EmployersSearch


class EmployerService:
    def __init__(self):
        self._data_layer = EmployerDataLayer()

    def create_employer(self, employer: EmployerCreate, current_user: str) -> JSONResponse:
        if not current_user:
            return JSONResponse(status_code=401, content="Unauthorized")

        new_employer = self._data_layer.create_employer(employer)
        return JSONResponse(content=f"Employer created successfully employer: {new_employer}",
                            status_code=201)

    def search_employers(self, employer_search: EmployersSearch,
                         current_user: str = None) -> JSONResponse:
        if not current_user:
            return JSONResponse(status_code=401, content="Unauthorized")

        employers = self._data_layer.search_employer(employer_search)
        return JSONResponse(content={"employers": employers}, status_code=200)
