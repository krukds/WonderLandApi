from datetime import time
from typing import Optional

from pydantic import BaseModel


class RestaurantResponse(BaseModel):
    id: int
    name: str
    phone: str
    description: str
    location_id: int
    open_at: time
    close_at: time
    menu_url: str
    main_photo: str


class RestaurantDetailResponse(BaseModel):
    id: int
    name: str
    phone: str
    description: str
    location: str
    open_at: time
    close_at: time
    menu_url: str
    photos: list[str]
    cuisines: list[str]
