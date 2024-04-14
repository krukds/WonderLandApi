from .base_service import BaseService
from ..base import async_session_maker
from ..models import SessionModel


class SessionService(BaseService[SessionModel]):
    model = SessionModel
    session_maker = async_session_maker

