from typing import Optional

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import Database

SessionLocal = Session(create_engine(Database.get().DATABASE_URL))


class RedisClient:
    _client: Optional[redis.Redis] = None

    @classmethod
    def get(cls):
        if cls._client is None:
            cls._client = redis.Redis(host='redis', port=6379, db=0)
        return cls._client


redis_client = RedisClient.get()
