from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from attractions_app.routes import get_attraction_by_id
from db.services.main_services import AttractionTicketServiceForAdmin, EventTicketServiceForAdmin, \
    AttractionServiceForManager

router = APIRouter(
    prefix="",
    tags=["Frontend"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/statistic-attractions")
async def statistic_page(
        request: Request
):
    return templates.TemplateResponse(
        request=request, name="statistics_for_attractions.html", context={}
    )


@router.get("/statistic-restaurants")
async def statistic_page(
        request: Request
):
    return templates.TemplateResponse(
        request=request, name="statistics_for_restaurants.html", context={}
    )


@router.get("/statistic-users")
async def statistic_page(
        request: Request
):
    return templates.TemplateResponse(
        request=request, name="statistics_for_users.html", context={}
    )


@router.get("/admin-logging")
async def admin_page(
        request: Request
):
    return templates.TemplateResponse(
        request=request, name="admin_page_logging.html", context={}
    )


@router.get("/admin-info")
async def admin_page(
        request: Request
):
    attraction_tickets = await AttractionTicketServiceForAdmin.select()
    event_tickets = await EventTicketServiceForAdmin.select()
    attractions = await AttractionServiceForManager.select()
    attractions_detail = []
    for attraction_id in range(len(list(attractions))):
        attraction_id += 1
        attraction = await get_attraction_by_id(attraction_id)
        attractions_detail.append(attraction)
    return templates.TemplateResponse(
        request=request,
        name="admin_page_info.html",
        context={"attraction_tickets": attraction_tickets, "event_tickets": event_tickets,
                 "attractions": attractions_detail}
    )
