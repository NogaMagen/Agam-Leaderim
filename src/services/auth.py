from fastapi.responses import JSONResponse

from data_layer.users import UsersDataLayer
from schemas.auth import UserCreate, LoginResponse
from security import create_access_token, hash_password, verify_password


class Authservice:
    def __init__(self):
        self._data_layer = UsersDataLayer()

    def sign_up(self, user: UserCreate) -> JSONResponse:
        user_by_username = self._data_layer.get_user_by_username(user.username)
        if user_by_username:
            return JSONResponse(content="username already registered")

        user.password = hash_password(user.password)
        self._data_layer.create_user(user)

        return JSONResponse(content="user created successfully")

    def log_in(self, user: UserCreate) -> JSONResponse | LoginResponse:

        user_by_username = self._data_layer.get_user_by_username(user.username)
        if user_by_username and verify_password(user.password, user_by_username.password):
            access_token = create_access_token(data={"sub": user.username})
            return LoginResponse(access_token=access_token, token_type="bearer")

        return JSONResponse(content="incorrect password or username")
