import datetime

import pytz
from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_404_NOT_FOUND

from auth_app import get_current_active_user
from db import AttractionTicketModel, UserModel, LoggingModel
from db.services import AttractionTicketServiceForUser, AttractionServiceForUser, LoggingServiceForAdmin
from utils import datetime_now
from .schemes import AttractionTicketPayload, AttractionTicketResponse

router = APIRouter(
    prefix="/attraction-tickets",
    tags=["Attraction tickets"]
)


@router.get("")
async def get_all_attraction_tickets(
        sort: int = -1,
        user: UserModel = Depends(get_current_active_user)
) -> list[AttractionTicketResponse]:
    attraction_tickets: list[AttractionTicketModel] = list(await AttractionTicketServiceForUser.select(user_id=user.id, order_by=(AttractionTicketModel.created_at if sort == -1 else AttractionTicketModel.created_at.desc())))
    if not attraction_tickets:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No attraction tickets found")

    attraction_tickets_response: list[AttractionTicketResponse] = [
        AttractionTicketResponse(
            created_at=(attraction_ticket.created_at + datetime.timedelta(hours=3)).strftime("%Y.%m.%d %H:%M:%S"),
            **attraction_ticket.dict(exclude=["created_at"]),
            title=(await AttractionServiceForUser.select_one(id=attraction_ticket.attraction_id)).name,
        ) for attraction_ticket in attraction_tickets
    ]

    return attraction_tickets_response


@router.post("")
async def add_attraction_ticket(
        payload: AttractionTicketPayload,
        user: UserModel = Depends(get_current_active_user)
):
    attraction_ticket: AttractionTicketModel = await AttractionTicketServiceForUser.save(
        AttractionTicketModel(
            **payload.model_dump(),
            user_id=user.id,
            created_at=datetime_now()
        )
    )

    logging = LoggingModel(
        role="User",
        log_time=datetime_now(),
        action_text=f"User {user.email} bought ticket for attraction with id{attraction_ticket.attraction_id}",
    )
    await LoggingServiceForAdmin.save(logging)

    return {"status": "ok"}
