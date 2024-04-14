from datetime import datetime

from fastapi import Depends, HTTPException
from jose import jwt
from pydantic import ValidationError
from starlette import status

from config import config
from db import UserService, UserModel, SessionModel
from db.services.sessions_service import SessionService
from utils import datetime_now
from .routes import oauth2_scheme
from .schemes import TokenPayload


async def get_current_active_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    try:
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

    session = await SessionService.select_one(
        SessionModel.access_token == token
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not find session",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserService.select_one(
        UserModel.id == session.user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not find user",
        )

    return user
