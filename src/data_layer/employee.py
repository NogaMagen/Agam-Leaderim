from data_layer import SessionLocal, redis_client
from data_layer.base import BaseDataLayer
from models import Employee, Employer, EmployeeToEmployer
from schemas.employee import EmployeeCreate, EmployeeAttachCreate


class EmployeeDataLayer(BaseDataLayer):
    def __init__(self):
        super().__init__(model=Employee, create_schema=EmployeeCreate, db_session=SessionLocal,
                         redis_client=redis_client)

    def attach_employee_to_employer(self, employee_attach: EmployeeAttachCreate) -> bool:

        employee = self._db.query(Employee).filter(Employee.id == employee_attach.employee_id).first()
        employer = self._db.query(Employer).filter(Employer.id == employee_attach.employer_id).first()

        if employee and employer:

            existing_association = self._db.query(EmployeeToEmployer).filter(
                EmployeeToEmployer.employee_id == employee_attach.employee_id,
                EmployeeToEmployer.employer_id == employee_attach.employer_id
            ).first()

            if not existing_association:

                new_association = EmployeeToEmployer(employee_id=employee_attach.employee_id,
                                                     employer_id=employee_attach.employer_id)
                self._db.add(new_association)
                self._db.commit()
                self._db.refresh(new_association)
                return True
            else:
                return False
        return False
