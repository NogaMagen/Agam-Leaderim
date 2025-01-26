from typing import Type, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import func, String
import json
from datetime import timedelta
from fastapi.encoders import jsonable_encoder

from models import Base


class BaseDataLayer:
    def __init__(self, model: Type[Base], create_schema: Type[BaseModel], db_session: Session, redis_client):
        self._db: Session = db_session
        self._redis = redis_client
        self.model = model
        self.create_schema = create_schema

    def create(self, schema: BaseModel) -> Base:
        new_instance = self.model(**schema.dict())
        self._db.add(new_instance)
        self._db.commit()
        self._db.refresh(new_instance)
        return new_instance

    def search(self, search_term: str, page: int = 1, per_page: int = 10) -> List[BaseModel]:
        cache_key = f"{self.model.__name__.lower()}_search:{search_term}:{page}:{per_page}"
        cached_data = self._redis.get(cache_key)

        if cached_data:
            return json.loads(cached_data)

        search_words = search_term.split()
        conditions = []

        for word in search_words:
            conditions.append(
                func.lower(self.model.first_name).like(f"%{word.lower()}%") |
                func.lower(self.model.last_name).like(f"%{word.lower()}%") |
                func.lower(self.model.position).like(f"%{word.lower()}%") |
                func.cast(self.model.government_id, String).like(f"%{word}%")
            )

        query = self._db.query(self.model).filter(*conditions)
        query = query.order_by(func.length(self.model.first_name).desc())
        query = query.offset((page - 1) * per_page).limit(per_page)

        instances = query.all()
        serialized_instances = [self.create_schema.from_orm(instance) for instance in instances]
        serialized_instances_dict = jsonable_encoder(serialized_instances)
        self._redis.setex(cache_key, timedelta(minutes=1), json.dumps(serialized_instances_dict))

        return serialized_instances_dict
