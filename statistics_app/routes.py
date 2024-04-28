from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Query
from starlette.status import HTTP_404_NOT_FOUND

from db import AttractionModel
from db.base import analyst_async_session_maker
from db.models import LocationModel, TagModel, AgeModel, AttractionTagModel, AttractionAgeModel
from db.services import AttractionServiceForUser
from db.services.main_services import (LocationServiceForUser, TagServiceForUser, AttractionTagServiceForUser, AttractionAgeServiceForUser,
                                       AgeServiceForUser, AttractionServiceForManager)
from .schemes import AttractionPayload, AttractionResponse, AttractionDetailResponse

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)

@router.get("/attraction-tickets-for-period/")
async def get_attractions_tickets_for_period(
    day: int = None,
    month: int = None,
    year: int = None
) -> list[dict]:
    try:
        async with analyst_async_session_maker() as session:
            query = text("""
                SELECT * FROM get_attraction_ticket_counts_for_period(:day, :month, :year) ORDER BY ticket_count DESC;
            """)
            result = await session.execute(query, {"day": day, "month": month, "year": year})
            await session.commit()
            attraction_ticket_counts = result.fetchall()
            return [{"attraction_id": row[0], "attraction_name": row[1], "ticket_count": row[2]} for row in attraction_ticket_counts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bookings-for-period/")
async def get_restaurant_bookings_for_period(
    day: int = None,
    month: int = None,
    year: int = None
) -> list[dict]:
    try:
        async with analyst_async_session_maker() as session:
            query = text("""
                SELECT * FROM get_restaurant_bookings_for_period(:day, :month, :year) ORDER BY booking_count DESC;
            """)
            result = await session.execute(query, {"day": day, "month": month, "year": year})
            await session.commit()
            restaurant_bookings_counts = result.fetchall()
            return [{"restaurant_id": row[0], "restaurant_name": row[1], "booking_count": row[2]} for row in restaurant_bookings_counts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_weekday_visits")
async def get_weekday_visits() -> list[dict]:
    try:
        async with analyst_async_session_maker() as session:
            query = text("""
                SELECT * FROM get_weekday_visits();
            """)
            result = await session.execute(query)
            await session.commit()
            visits_count = result.fetchall()
            return [{"weekday": row[0], "visits_count": row[1]} for row in visits_count]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_hourly_visits")
async def get_hourly_visits() -> list[dict]:
    try:
        async with analyst_async_session_maker() as session:
            query = text("""
                SELECT * FROM get_hourly_visits();
            """)
            result = await session.execute(query)
            await session.commit()
            visits_count = result.fetchall()
            return [{"hour": row[0], "visits_count": row[1]} for row in visits_count]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))