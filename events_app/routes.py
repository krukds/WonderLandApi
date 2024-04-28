from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from db.models import EventModel, LocationModel
from db.services.main_services import EventServiceForUser, LocationServiceForUser
from .schemes import EventResponse, EventDetailResponse

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get("")
async def get_all_events() -> list[EventResponse]:
    events = await EventServiceForUser.select()
    if not events:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No events found")

    events_response: list[EventResponse] = [
        EventResponse(
            **event.dict(exclude=["start_at", "end_at"]),
            start_at=event.start_at.strftime("%Y-%m-%d %H:%M:%S"),
            end_at=event.end_at.strftime("%Y-%m-%d %H:%M:%S"),
        ) for event in events
    ]

    return events_response


@router.get("/{event_id}")
async def get_event_by_id(
        event_id: int
) -> EventDetailResponse:
    event: EventModel = await EventServiceForUser.select_one(
        EventModel.id == event_id
    )
    if not event:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No event with this id found")

    location = await LocationServiceForUser.select_one(LocationModel.id == event.location_id)
    if not location:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No location")

    return EventDetailResponse(
        **event.dict(exclude=["start_at", "end_at"]),
        location=location.name,
        start_at=event.start_at.strftime("%Y-%m-%d %H:%M:%S"),
        end_at=event.end_at.strftime("%Y-%m-%d %H:%M:%S"),
    )
