from datetime import datetime

from pydantic import BaseModel, NaiveDatetime


class AttractionTicketPayload(BaseModel):
    attraction_id: int
    is_expired: bool


class AttractionTicketResponse(BaseModel):
    id: int
    title: str
    is_expired: bool
    created_at: NaiveDatetime
