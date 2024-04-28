from datetime import datetime

from pydantic import BaseModel, NaiveDatetime


class EventTicketPayload(BaseModel):
    event_id: int
    is_expired: bool


class EventTicketResponse(BaseModel):
    id: int
    title: str
    is_expired: bool
    created_at: str
