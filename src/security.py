from datetime import datetime, timezone
from datetime import timedelta

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config import Encoding, JWT
from schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=JWT.get().ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, JWT.get().SECRET_KEY, algorithm=JWT.get().ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode(Encoding.ENCODE_METHOD),
        hashed_password.encode(Encoding.ENCODE_METHOD)
    )


def hash_password(password: str) -> str:
    password_bytes = password.encode(Encoding.ENCODE_METHOD)
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password.decode(Encoding.ENCODE_METHOD)


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = jwt.decode(token, key=JWT.get().SECRET_KEY, algorithms=[JWT.get().ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

        if "exp" in payload:
            exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            if datetime.now(timezone.utc) >= exp:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        return TokenData(username=username)

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate token")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Error: {str(e)}")
