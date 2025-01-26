from data_layer.base import BaseDataLayer
from data_layer import SessionLocal, redis_client
from models import Employer
from schemas.employer import EmployerCreate


class EmployerDataLayer(BaseDataLayer):
    def __init__(self):
        super().__init__(model=Employer, create_schema=EmployerCreate, db_session=SessionLocal,
                         redis_client=redis_client)
