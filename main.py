from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, Depends

import auth_app


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title="Wonder Land Api",
    lifespan=lifespan
)

secured_router = APIRouter(
    dependencies=[Depends(auth_app.get_current_active_user)]
)

api_router = APIRouter(
    prefix="/api",
    # dependencies=[Depends(auth_app.auth_secure)]

)
api_router.include_router(auth_app.router)
app.include_router(secured_router)
app.include_router(api_router)

