from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from starlette import status

from config import config
from db import UserModel, SessionModel
from db.services import UserServiceForManager, SessionServiceForManager
from utils import datetime_now
from .schemes import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)


async def get_current_active_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    try:
        print(token)
        payload = jwt.decode(
            token, config.JWT_SECRET_KEY.get_secret_value(), algorithms=[config.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.expires_at) < datetime_now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    session = await SessionServiceForManager.select_one(
        SessionModel.access_token == token
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not find session",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserServiceForManager.select_one(
        UserModel.id == session.user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not find user",
        )

    return user
