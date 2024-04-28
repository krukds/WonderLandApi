from datetime import datetime

from pydantic import BaseModel, NaiveDatetime, AwareDatetime


class AttractionTicketPayload(BaseModel):
    attraction_id: int
    is_expired: bool


class AttractionTicketResponse(BaseModel):
    id: int
    title: str
    is_expired: bool
    created_at: str
