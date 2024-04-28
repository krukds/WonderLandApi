from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_404_NOT_FOUND


from db.services import TagServiceForUser
from .schemes import TagResponse

router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)


@router.get("")
async def get_all_tags(
) -> list[TagResponse]:
    tags = await TagServiceForUser.select()
    if not tags:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No tags found")

    return tags

