from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from db.models import EventModel
from db.services.main_services import EventService
from .schemes import EventResponse

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get("")
async def get_all_events() -> list[EventResponse]:
    events = await EventService.select()
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
) -> EventResponse:
    event: EventModel = await EventService.select_one(
        EventModel.id == event_id
    )
    if not event:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No event with this id found")

    return EventResponse(
        **event.dict(exclude=["start_at", "end_at"]),
        start_at=event.start_at.strftime("%Y-%m-%d %H:%M:%S"),
        end_at=event.end_at.strftime("%Y-%m-%d %H:%M:%S"),
    )
