from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import ValidationError
from starlette import status

from db import UserModel, UserService
from .schemes import TokenResponse, SignupPayload, LoginPayload
from .utils import create_user_session

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


@router.post("/login")
async def login(
        payload: LoginPayload = Depends()
) -> TokenResponse:
    user = await UserService.select_one(
        UserModel.email == payload.email,
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
