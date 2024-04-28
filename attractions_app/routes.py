import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Query
from starlette.status import HTTP_404_NOT_FOUND

from db import AttractionModel
from db.base import analyst_async_session_maker
from db.models import LocationModel, TagModel, AgeModel, AttractionTagModel, AttractionAgeModel, LoggingModel
from db.services import AttractionServiceForUser
from db.services.main_services import (LocationServiceForUser, TagServiceForUser, AttractionTagServiceForUser,
                                       AttractionAgeServiceForUser,
                                       AgeServiceForUser, AttractionServiceForManager, LoggingServiceForAdmin)
from .schemes import AttractionPayload, AttractionResponse, AttractionDetailResponse

router = APIRouter(
    prefix="/attractions",
    tags=["Attractions"]
)


@router.get("")
async def get_all_attractions(
        tag_names: str = None,
        age_names: str = None
) -> list[AttractionResponse]:
    attractions = await AttractionServiceForUser.select()
    if not attractions:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No attractions found")

    base_query = select(AttractionModel)

    if tag_names and tag_names.split(','):
        tag_names = tag_names.split(",")
        tag_ids = [tag.id for tag in (await TagServiceForUser.select(TagModel.name.in_(tag_names)))] if tag_names else []
        base_query = base_query.where(AttractionModel.id.in_(
            select(AttractionTagModel.attraction_id).where(AttractionTagModel.tag_id.in_(tag_ids))
        ))

    if age_names and age_names.split(','):
        age_names = age_names.split(",")
        age_ids = [age.id for age in (await AgeServiceForUser.select(AgeModel.name.in_(age_names)))] if age_names else []
        base_query = base_query.where(AttractionModel.id.in_(
            select(AttractionAgeModel.attraction_id).where(AttractionAgeModel.age_id.in_(age_ids))
        ))

    attractions = await AttractionServiceForUser.execute(base_query)

    if not attractions:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No attractions found")

    return attractions


@router.post("")
async def add_attraction(
        payload: AttractionPayload
) -> AttractionResponse:
    attraction: AttractionModel = await AttractionServiceForManager.save(
        AttractionModel(**payload.model_dump())
    )
    logging = LoggingModel(
        role="Manager",
        log_time=datetime_now(),
        action_text=f"Manager added attraction '{attraction.name}'",
    )
    await LoggingServiceForAdmin.save(logging)
    return AttractionResponse(**attraction.__dict__)


@router.get("/{attraction_id}")
async def get_attraction_by_id(
        attraction_id: int
) -> AttractionDetailResponse:
    attraction: AttractionModel = await AttractionServiceForUser.select_one(
        AttractionModel.id == attraction_id
    )
    if not attraction:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No attraction with this id found")

    location = await LocationServiceForUser.select_one(LocationModel.id == attraction.location_id)
    if not location:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No location")

    attraction_tag_pairs = await AttractionTagServiceForUser.select(attraction_id=attraction_id)
    tags_ids = [item.tag_id for item in attraction_tag_pairs]
    tags = await TagServiceForUser.select(TagModel.id.in_(tags_ids))

    attraction_age_pairs = await AttractionAgeServiceForUser.select(attraction_id=attraction_id)
    ages_ids = [item.age_id for item in attraction_age_pairs]
    ages = await AgeServiceForUser.select(AgeModel.id.in_(ages_ids))

    return AttractionDetailResponse(
        **attraction.__dict__,
        location=location.name,
        tags=[item.name for item in tags],
        ages=[item.name for item in ages]
    )


@router.put("/{attraction_id}")
async def update_attraction(
        attraction_id: int,
        payload: AttractionPayload
) -> AttractionResponse:
    attraction: AttractionModel = await AttractionServiceForManager.select_one(
        AttractionModel.id == attraction_id
    )
    if not attraction:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No attraction with this id found")

    for key, value in payload.model_dump().items():
        setattr(attraction, key, value)

    updated_attraction = await AttractionServiceForManager.save(attraction)
    logging = LoggingModel(
        role="Manager",
        log_time=datetime_now(),
        action_text=f"Manager updated attraction '{updated_attraction.name}'",
    )
    await LoggingServiceForAdmin.save(logging)
    return AttractionResponse(**updated_attraction.__dict__)


@router.delete("/{attraction_id}")
async def delete_attraction(
        attraction_id: int
):
    attraction: AttractionModel = await AttractionServiceForManager.select_one(
        AttractionModel.id == attraction_id
    )
    if not attraction:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No attraction with this id found")
    await AttractionServiceForManager.delete(id=attraction_id)
    logging = LoggingModel(
        role="Manager",
        log_time=datetime_now(),
        action_text=f"Manager deleted attraction '{attraction.name}'",
    )
    await LoggingServiceForAdmin.save(logging)
    return {"status": "success"}

