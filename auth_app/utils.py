from datetime import datetime, timedelta

from jose import jwt

from config import config
from db import UserModel, SessionModel
from db.services import SessionService
from utils import datetime_now, timestamp_now


def create_access_token(user_id: int, expires_at: datetime = None) -> str:
    if expires_at is None:
        expires_at = generate_access_token_expires_at()
    to_encode = {"expires_at": int(expires_at.timestamp()), "user_id": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET_KEY.get_secret_value(), config.ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: int, expires_at: datetime = None) -> str:
    if expires_at is None:
        expires_at = generate_refresh_token_expires_at()

    to_encode = {"expires_at": int(expires_at.timestamp()), "user_id": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, config.JWT_REFRESH_SECRET_KEY.get_secret_value(), config.ALGORITHM)
    return encoded_jwt


def generate_access_token_expires_at() -> datetime:
    return datetime_now() + timedelta(days=1)
    # expires_at = int((datetime_now() + timedelta(seconds=10 * 60 * 60 * 60)).timestamp())
    # return expires_at


def generate_refresh_token_expires_at() -> int:
    expires_at = int((datetime.utcnow() + timedelta(seconds=10 * 60 * 60 * 60)).timestamp())
    return expires_at


async def create_user_session(user_id: int) -> SessionModel:
    access_token_expires_at = generate_access_token_expires_at()
    session = SessionModel(
        user_id=user_id,
        access_token=create_access_token(user_id, access_token_expires_at),
        expires_at=access_token_expires_at
    )
    await SessionService.save(session)
    return session
