import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from starlette import status
from starlette.status import HTTP_404_NOT_FOUND

from db import UserModel, LoggingModel
from db.services import (UserServiceForManager, LoggingServiceForAdmin)
from utils import datetime_now
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
    user = await UserServiceForManager.select_one(
        UserModel.email == payload.username,
        UserModel.password == payload.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    session = await create_user_session(user.id)
    logging = LoggingModel(
        role="User",
        log_time=datetime_now(),
        action_text=f"User {user.email} logged in",
    )
    await LoggingServiceForAdmin.save(logging)

    return TokenResponse(
        access_token=session.access_token,
        refresh_token=None
    )


@router.post("/signup")
async def signup(
        payload: SignupPayload
) -> TokenResponse:
    user = await UserServiceForManager.select_one(
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
            await UserServiceForManager.save(user)

        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect payload data"
            )

    session = await create_user_session(user.id)

    logging = LoggingModel(
        role="User",
        log_time=datetime_now(),
        action_text=f"User {user.email} signed up",
    )
    await LoggingServiceForAdmin.save(logging)

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
    await UserServiceForManager.delete(id=user.id)

    logging = LoggingModel(
        role="User",
        log_time=datetime_now(),
        action_text=f"User {user.email} deleted account",
    )
    await LoggingServiceForAdmin.save(logging)

    return {"status": "ok"}


@router.put("/me")
async def update_me(
        payload: UserPayload,
        user: UserModel = Depends(get_current_active_user)
) -> UserResponse:
    user: UserModel = await UserServiceForManager.select_one(
        UserModel.id == user.id
    )
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No user with this id found")

    for key, value in payload.model_dump().items():
        setattr(user, key, value)

    updated_user = await UserServiceForManager.save(user)

    logging = LoggingModel(
        role="User",
        log_time=datetime_now(),
        action_text=f"User {user.email} updated account",
    )
    await LoggingServiceForAdmin.save(logging)

    return UserResponse(**updated_user.__dict__)
