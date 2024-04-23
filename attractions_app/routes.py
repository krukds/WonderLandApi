from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Query
from starlette.status import HTTP_404_NOT_FOUND

from db import AttractionModel
from db.models import LocationModel, TagModel, AgeModel, AttractionTagModel, AttractionAgeModel
from db.services import AttractionService
from db.services.main_services import LocationService, TagService, AttractionTagService, AttractionAgeService, AgeService
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
    attractions = await AttractionService.select()
    if not attractions:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No attractions found")

    base_query = select(AttractionModel)

    if tag_names and tag_names.split(','):
        tag_names = tag_names.split(",")
        tag_ids = [tag.id for tag in (await TagService.select(TagModel.name.in_(tag_names)))] if tag_names else []
        base_query = base_query.where(AttractionModel.id.in_(
            select(AttractionTagModel.attraction_id).where(AttractionTagModel.tag_id.in_(tag_ids))
        ))

    if age_names and age_names.split(','):
        age_names = age_names.split(",")
        age_ids = [age.id for age in (await AgeService.select(AgeModel.name.in_(age_names)))] if age_names else []
        base_query = base_query.where(AttractionModel.id.in_(
            select(AttractionAgeModel.attraction_id).where(AttractionAgeModel.age_id.in_(age_ids))
        ))

    attractions = await AttractionService.execute(base_query)

    if not attractions:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No attractions found")

    return attractions


@router.post("")
async def add_attraction(
        payload: AttractionPayload
) -> AttractionResponse:
    attraction: AttractionModel = await AttractionService.save(
        AttractionModel(**payload.model_dump())
    )
    return AttractionResponse(**attraction.__dict__)


@router.get("/{attraction_id}")
async def get_attraction_by_id(
        attraction_id: int
) -> AttractionDetailResponse:
    attraction: AttractionModel = await AttractionService.select_one(
        AttractionModel.id == attraction_id
    )
    if not attraction:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No attraction with this id found")

    location = await LocationService.select_one(LocationModel.id == attraction.location_id)
    if not location:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No location")

    attraction_tag_pairs = await AttractionTagService.select(attraction_id=attraction_id)
    tags_ids = [item.tag_id for item in attraction_tag_pairs]
    tags = await TagService.select(TagModel.id.in_(tags_ids))

    attraction_age_pairs = await AttractionAgeService.select(attraction_id=attraction_id)
    ages_ids = [item.age_id for item in attraction_age_pairs]
    ages = await AgeService.select(AgeModel.id.in_(ages_ids))

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
    attraction: AttractionModel = await AttractionService.select_one(
        AttractionModel.id == attraction_id
    )
    if not attraction:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No attraction with this id found")

    for key, value in payload.model_dump().items():
        setattr(attraction, key, value)

    updated_attraction = await AttractionService.save(attraction)
    return AttractionResponse(**updated_attraction.__dict__)


@router.delete("/{attraction_id}")
async def delete_attraction(
        attraction_id: int
):
    attraction: AttractionModel = await AttractionService.select_one(
        AttractionModel.id == attraction_id
    )
    if not attraction:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No attraction with this id found")
    await AttractionService.delete(id=attraction_id)

    return {"status": "success"}
