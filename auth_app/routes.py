from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from starlette import status
from starlette.status import HTTP_404_NOT_FOUND

from db import UserModel
from db.services import (UserService, AttractionTicketService, EventTicketService, SessionService,
                         RestaurantTableBookingService, AttractionReviewService)
from .deps import get_current_active_user
from .schemes import TokenResponse, SignupPayload, UserResponse, UserPayload
from .utils import create_user_session

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)


@router.post("/login")
async def login(
        payload: OAuth2PasswordRequestForm = Depends()
) -> TokenResponse:
    user = await UserService.select_one(
        UserModel.email == payload.username,
        UserModel.password == payload.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    session = await create_user_session(user.id)
    return TokenResponse(
        access_token=session.access_token,
        refresh_token=None
    )


@router.post("/signup")
async def signup(
        payload: SignupPayload
) -> TokenResponse:
    user = await UserService.select_one(
        UserModel.email == payload.email
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already used"
        )
    else:
        try:
            user = UserModel(
                **payload.model_dump()
            )
            await UserService.save(user)

        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect payload data"
            )

    session = await create_user_session(user.id)
    return TokenResponse(
        access_token=session.access_token,
        refresh_token=None
    )


@router.get("/me")
async def get_me(
        user: UserModel = Depends(get_current_active_user)
) -> UserResponse:
    return UserResponse(**user.dict())


@router.delete("/me")
async def delete_me(
        user: UserModel = Depends(get_current_active_user)
):
    # await AttractionReviewService.delete(user_id=user.id)
    # await RestaurantTableBookingService.delete(user_id=user.id)
    # await AttractionTicketService.delete(user_id=user.id)
    # await EventTicketService.delete(user_id=user.id)
    # await SessionService.delete(user_id=user.id)
    await UserService.delete(id=user.id)
    return {"status": "ok"}

@router.put("/me")
async def update_me(
        payload: UserPayload,
        user: UserModel = Depends(get_current_active_user)
) -> UserResponse:
    user: UserModel = await UserService.select_one(
        UserModel.id == user.id
    )
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No user with this id found")

    for key, value in payload.model_dump().items():
        setattr(user, key, value)

    updated_user = await UserService.save(user)
    return UserResponse(**updated_user.__dict__)
