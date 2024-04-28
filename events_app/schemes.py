from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.v1 import validator


class EventPayload(BaseModel):
    name: str
    description: str
    start_at: datetime
    end_at: datetime
    price: int
    photo_url: str
    location_id: int

    @validator('start_at', 'end_at', pre=True)
    def parse_date(cls, value: str):
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


class EventResponse(BaseModel):
    id: int
    name: str
    description: str
    start_at: str
    end_at: str
    price: int
    photo_url: str
    location_id: int


class EventDetailResponse(BaseModel):
    id: int
    name: str
    description: str
    start_at: str
    end_at: str
    price: int
    photo_url: str
    location: str


