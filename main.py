from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, Depends

import auth_app, attractions_app, attraction_tickets_app, events_app, event_tickets_app, \
    restaurants_app, tags_app, ages_app, frontend_app, statistics_app, logging_app


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title="Wonder Land Api",
    lifespan=lifespan
)

secured_router = APIRouter(
    prefix="/api",
    dependencies=[Depends(auth_app.get_current_active_user)]
)

api_router = APIRouter(
    prefix="/api",
    # dependencies=[Depends(auth_app.auth_secure)]

)
api_router.include_router(auth_app.router)
api_router.include_router(attractions_app.router)
secured_router.include_router(attraction_tickets_app.router)
api_router.include_router(events_app.router)
secured_router.include_router(event_tickets_app.router)
api_router.include_router(restaurants_app.router)
api_router.include_router(tags_app.router)
api_router.include_router(ages_app.router)
api_router.include_router(statistics_app.router)
api_router.include_router(logging_app.router)
app.include_router(api_router)
app.include_router(secured_router)
app.include_router(frontend_app.router)

