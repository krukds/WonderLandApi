import datetime

from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_404_NOT_FOUND

from auth_app import get_current_active_user
from db import EventTicketModel, UserModel, LoggingModel
from db.services import EventTicketServiceForUser, EventServiceForUser, LoggingServiceForAdmin
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
    event_tickets = await EventTicketServiceForUser.select(user_id=user.id, order_by=(EventTicketModel.created_at if sort == -1 else EventTicketModel.created_at.desc()))
    if not event_tickets:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No event tickets found")

    event_tickets_response: list[EventTicketResponse] = [
        EventTicketResponse(
            **event_ticket.dict(exclude=["created_at"]),
            created_at=(event_ticket.created_at + datetime.timedelta(hours=3)).strftime("%Y.%m.%d %H:%M:%S"),
            title=(await EventServiceForUser.select_one(id=event_ticket.event_id)).name,
        ) for event_ticket in event_tickets
    ]

    return event_tickets_response


@router.post("")
async def add_event_ticket(
        payload: EventTicketPayload,
        user: UserModel = Depends(get_current_active_user)
):
    event_ticket: EventTicketModel = await EventTicketServiceForUser.save(
        EventTicketModel(
            **payload.model_dump(),
            user_id=user.id,
            created_at=datetime_now()
        )
    )

    logging = LoggingModel(
        role="User",
        log_time=datetime_now(),
        action_text=f"User {user.email} bought ticket for event with id{event_ticket.event_id}",
    )
    await LoggingServiceForAdmin.save(logging)

    return {"status": "ok"}
