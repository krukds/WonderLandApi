from db import UserModel, SessionModel
from db.base import async_session_maker
from db.services.base_service import BaseService


class UserService(BaseService[UserModel]):
    model = UserModel
    session_maker = async_session_maker


class SessionService(BaseService[SessionModel]):
    model = SessionModel
    session_maker = async_session_maker
