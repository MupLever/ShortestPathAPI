from jwt import InvalidTokenError
from fastapi import Form, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette import status

from api_v1.auth import crud
from app.models import User

from configs.database import get_session_dependency
from utils import auth

http_bearer = HTTPBearer()


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: Session = Depends(get_session_dependency),
) -> User:
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
    )
    token = creds.credentials
    try:
        payload = auth.decode_jwt(token=token)
    except InvalidTokenError:
        raise unauthed_exception

    if user := crud.get_user_by_username(session, payload["username"]):
        return user

    raise unauthed_exception


def check_user(
    email: str = Form(),
    password: str = Form(),
    session: Session = Depends(get_session_dependency),
):
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password"
    )
    if not (user := crud.get_user_by_email(session, email)):
        raise unauthed_exception

    if auth.check_password(password, user.password) and user.is_active:
        return user

    raise unauthed_exception
