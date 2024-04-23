from datetime import datetime

from pydantic import BaseModel


class TagResponse(BaseModel):
    id: int
    name: str
