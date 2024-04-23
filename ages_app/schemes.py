from datetime import datetime

from pydantic import BaseModel


class AgeResponse(BaseModel):
    id: int
    name: str
