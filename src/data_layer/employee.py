import json
from datetime import timedelta
from typing import List

from sqlalchemy import func, String
from sqlalchemy.orm import Session

from data_layer import SessionLocal, redis_client
from models import Employee, Employer, EmployeeToEmployer
from schemas.create import EmployeeCreate


class EmployeeDataLayer:
    def __init__(self):
        self._db: Session = SessionLocal
        self._redis = redis_client

    def create_employee(self, employee: EmployeeCreate) -> Employee:
        new_employee = Employee(**employee.dict())
        self._db.add(new_employee)
        self._db.commit()
        self._db.refresh(new_employee)
        return new_employee

    def search_employee(self, search_term: str, page: int = 1, per_page: int = 10) -> List[Employee]:

        cache_key = f"employee_search:{search_term}:{page}:{per_page}"
        cached_data = self._redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        query = self._db.query(Employee).filter(
            func.lower(Employee.first_name).like(f"%{search_term.lower()}%") |
            func.lower(Employee.last_name).like(f"%{search_term.lower()}%") |
            func.lower(Employee.position).like(f"%{search_term.lower()}%") |
            func.cast(Employee.government_id, String).like(f"%{search_term}%")
        )

        query = query.offset((page - 1) * per_page).limit(per_page)
        employees = query.all()

        self._redis.setex(cache_key, timedelta(minutes=1), json.dumps([employee.to_dict() for employee in employees]))

        return employees

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
