from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import Database

SessionLocal = Session(create_engine(Database.get().DATABASE_URL))
