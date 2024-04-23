from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_404_NOT_FOUND


from db.services import AgeService
from .schemes import AgeResponse

router = APIRouter(
    prefix="/ages",
    tags=["Ages"]
)


@router.get("")
async def get_all_ages(
) -> list[AgeResponse]:
    ages = await AgeService.select()
    if not ages:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No ages found")

    return ages

