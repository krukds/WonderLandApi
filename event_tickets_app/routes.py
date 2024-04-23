from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_404_NOT_FOUND

from auth_app import get_current_active_user
from db import EventTicketModel, UserModel
from db.services import EventTicketService, EventService
from utils import datetime_now
from .schemes import EventTicketPayload, EventTicketResponse

router = APIRouter(
    prefix="/event-tickets",
    tags=["Event tickets"]
)


@router.get("")
async def get_all_event_tickets(
        sort: int = -1,
        user: UserModel = Depends(get_current_active_user)
) -> list[EventTicketResponse]:
    event_tickets = await EventTicketService.select(user_id=user.id, order_by=(EventTicketModel.created_at if sort == -1 else EventTicketModel.created_at.desc()))
    if not event_tickets:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No event tickets found")

    event_tickets_response: list[EventTicketResponse] = [
        EventTicketResponse(
            **event_ticket.dict(),
            title=(await EventService.select_one(id=event_ticket.event_id)).name,
        ) for event_ticket in event_tickets
    ]

    return event_tickets_response


@router.post("")
async def add_event_ticket(
        payload: EventTicketPayload,
        user: UserModel = Depends(get_current_active_user)
):
    event_ticket: EventTicketModel = await EventTicketService.save(
        EventTicketModel(
            **payload.model_dump(),
            user_id=user.id,
            created_at=datetime_now()
        )
    )
    return {"status": "ok"}
