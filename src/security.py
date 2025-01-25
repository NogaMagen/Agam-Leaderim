from datetime import datetime, timedelta
from typing import Union

import bcrypt
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from config import Hashing, JWT

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    username: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=JWT.get().ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT.get().SECRET_KEY, algorithm=JWT.get().ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)) -> Union[TokenData, JSONResponse]:
    try:
        payload = jwt.decode(token, Hashing.get().SECRET_KEY, algorithms=[Hashing.get().ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            return JSONResponse(status_code=401, content="Could not validate credentials")

        return TokenData(username=username)

    except JWTError:
        return JSONResponse(status_code=401, content="Could not validate credentials")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(Hashing.get().ENCODE_METHOD),
                          hashed_password.encode(Hashing.get().ENCODE_METHOD))


def hash_password(password: str) -> str:
    password_bytes = password.encode(Hashing.get().ENCODE_METHOD)
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password.decode(Hashing.get().ENCODE_METHOD)
