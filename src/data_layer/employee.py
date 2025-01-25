from typing import List, Dict

from sqlalchemy.orm import Session

from data_layer import SessionLocal
from models import Employee, Employer, EmployeeToEmployer
from schemas.create import EmployeeCreate


class EmployeeDataLayer:
    def __init__(self):
        self._db: Session = SessionLocal

    def create_employee(self, employee: EmployeeCreate) -> Employee:
        new_employee = Employee(**employee.dict())
        self._db.add(new_employee)
        self._db.commit()
        self._db.refresh(new_employee)
        return new_employee

    def search_employee(self, filters: Dict[str, str | int]) -> List[Employee]:
        query = self._db.query(Employee)
        for key, value in filters.items():
            query = query.filter(getattr(Employee, key) == value)
        return query.all()

    def attach_employee_to_employer(self, employee_id: int, employer_id: int) -> bool:

        employee = self._db.query(Employee).filter(Employee.id == employee_id).first()
        employer = self._db.query(Employer).filter(Employer.id == employer_id).first()

        if employee and employer:

            existing_association = self._db.query(EmployeeToEmployer).filter(
                EmployeeToEmployer.employee_id == employee_id,
                EmployeeToEmployer.employer_id == employer_id
            ).first()

            if not existing_association:

                new_association = EmployeeToEmployer(employee_id=employee_id, employer_id=employer_id)
                self._db.add(new_association)
                self._db.commit()
                self._db.refresh(new_association)
                return True
            else:
                return False
        return False
