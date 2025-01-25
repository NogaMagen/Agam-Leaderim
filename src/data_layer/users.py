from typing import Optional

from sqlalchemy.orm import Session

from data_layer import SessionLocal
from models import User
from schemas.create import UserCreate


class UsersDataLayer:
    def __init__(self):
        self._db: Session = SessionLocal

    def create_user(self, user: UserCreate) -> User:
        new_user = User(**user.dict())
        self._db.add(new_user)
        self._db.commit()
        self._db.refresh(new_user)
        return new_user

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self._db.query(User).filter(User.username == username).first()
