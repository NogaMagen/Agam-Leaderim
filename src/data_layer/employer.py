from typing import List, Dict

from sqlalchemy.orm import Session

from data_layer import SessionLocal
from models import Employer
from schemas.create import EmployerCreate


class EmployerDataLayer:
    def __init__(self):
        self._db: Session = SessionLocal

    def create_employer(self, employer: EmployerCreate) -> Employer:
        new_employer = Employer(**employer.dict())
        self._db.add(new_employer)
        self._db.commit()
        self._db.refresh(new_employer)
        return new_employer

    def search_employer(self, filters: Dict[str, str | int]) -> List[Employer]:
        query = self._db.query(Employer)
        for key, value in filters.items():
            query = query.filter(getattr(Employer, key) == value)
        return query.all()
