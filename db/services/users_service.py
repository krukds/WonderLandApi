from .base_service import BaseService
from ..base import async_session_maker
from ..models import UserModel


class UserService(BaseService[UserModel]):
    model = UserModel
    session_maker = async_session_maker

