from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_404_NOT_FOUND


from db.services import LoggingServiceForAdmin
from .schemes import LoggingResponse

router = APIRouter(
    prefix="/logging",
    tags=["Logging"]
)


@router.get("")
async def get_all_logging(
) -> list[LoggingResponse]:
    logging = await LoggingServiceForAdmin.select()
    if not logging:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No logging found")

    return logging

