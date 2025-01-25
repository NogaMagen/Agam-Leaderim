import json
from datetime import timedelta
from typing import List

from sqlalchemy import func, String
from sqlalchemy.orm import Session

from data_layer import SessionLocal, redis_client
from models import Employer
from schemas.employer import EmployerCreate, EmployersSearch


class EmployerDataLayer:
    def __init__(self):
        self._db: Session = SessionLocal
        self._redis = redis_client

    def create_employer(self, employer: EmployerCreate) -> Employer:
        new_employer = Employer(**employer.dict())
        self._db.add(new_employer)
        self._db.commit()
        self._db.refresh(new_employer)
        return new_employer

    def search_employer(self, employers_search: EmployersSearch) -> List[Employer]:
        cache_key = f"employer_search:{employers_search.search_term}:{employers_search.page}:{employers_search.per_page}"
        cached_data = self._redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        query = self._db.query(Employer).filter(
            func.lower(Employer.name).like(f"%{employers_search.search_term.lower()}%") |
            func.cast(Employer.government_id, String).like(f"%{employers_search.search_term}%")
        )

        query = query.offset((employers_search.page - 1) * employers_search.per_page).limit(employers_search.per_page)
        employers = query.all()

        self._redis.setex(cache_key, timedelta(minutes=1), json.dumps([employer.to_dict() for employer in employers]))

        return employers
