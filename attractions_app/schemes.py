from typing import Optional

from pydantic import BaseModel


class AttractionPayload(BaseModel):
    location_id: int
    name: str
    description: str
    price: int
    duration: int
    minimum_height: float
    photo_url: str


class AttractionResponse(BaseModel):
    id: int
    location_id: int
    name: str
    description: str
    price: int
    duration: int
    minimum_height: float
    photo_url: str


class AttractionDetailResponse(BaseModel):
    id: int
    location: str
    name: str
    description: str
    price: int
    duration: int
    minimum_height: float
    photo_url: str
    tags: list[str]
    ages: list[str]
