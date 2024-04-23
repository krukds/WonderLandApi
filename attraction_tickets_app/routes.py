from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_404_NOT_FOUND

from auth_app import get_current_active_user
from db import AttractionTicketModel, UserModel
from db.services import AttractionTicketService, AttractionService
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
    attraction_tickets = await AttractionTicketService.select(user_id=user.id, order_by=(AttractionTicketModel.created_at if sort == -1 else AttractionTicketModel.created_at.desc()))
    if not attraction_tickets:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No attraction tickets found")

    attraction_tickets_response: list[AttractionTicketResponse] = [
        AttractionTicketResponse(
            **attraction_ticket.dict(),
            title=(await AttractionService.select_one(id=attraction_ticket.attraction_id)).name,
        ) for attraction_ticket in attraction_tickets
    ]

    return attraction_tickets_response


@router.post("")
async def add_attraction_ticket(
        payload: AttractionTicketPayload,
        user: UserModel = Depends(get_current_active_user)
):
    attraction_ticket: AttractionTicketModel = await AttractionTicketService.save(
        AttractionTicketModel(
            **payload.model_dump(),
            user_id=user.id,
            created_at=datetime_now()
        )
    )
    return {"status": "ok"}
