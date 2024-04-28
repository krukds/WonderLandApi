from datetime import datetime

from pydantic import BaseModel, NaiveDatetime


class LoggingResponse(BaseModel):
    role: str
    log_time: NaiveDatetime
    action_text: str
