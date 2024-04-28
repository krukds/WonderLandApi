from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from starlette.status import HTTP_404_NOT_FOUND

from db.base import analyst_async_session_maker
from db.models import LocationModel, RestaurantModel, CuisineModel
from db.services import RestaurantServiceForUser, LocationServiceForUser, RestaurantCuisineServiceForUser, CuisineServiceForUser, \
    RestaurantPhotoServiceForUser
from .schemes import RestaurantResponse, RestaurantDetailResponse

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)


@router.get("")
async def get_all_restaurants() -> list[RestaurantResponse]:
    restaurants = await RestaurantServiceForUser.select()
    if not restaurants:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No restaurants found")

    restaurants_response = []

    for restaurant in restaurants:
        photo = await RestaurantPhotoServiceForUser.select_one(restaurant_id=restaurant.id)
        restaurant_res = RestaurantResponse(
            **restaurant.dict(),
            main_photo=photo.url
        )
        restaurants_response.append(restaurant_res)

    return restaurants_response


@router.get("/{restaurant_id}")
async def get_restaurant_by_id(
        restaurant_id: int
) -> RestaurantDetailResponse:
    restaurant: RestaurantModel = await RestaurantServiceForUser.select_one(
        RestaurantModel.id == restaurant_id
    )
    if not restaurant:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No restaurant with this id found")

    location = await LocationServiceForUser.select_one(LocationModel.id == restaurant.location_id)
    if not location:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No location")

    restaurant_cuisine_pairs = await RestaurantCuisineServiceForUser.select(restaurant_id=restaurant_id)
    cuisines_ids = [item.cuisine_id for item in restaurant_cuisine_pairs]
    cuisines = await CuisineServiceForUser.select(CuisineModel.id.in_(cuisines_ids))

    photos = await RestaurantPhotoServiceForUser.select(restaurant_id=restaurant_id)

    return RestaurantDetailResponse(
        **restaurant.__dict__,
        location=location.name,
        photos=[item.url for item in photos],
        cuisines=[item.name for item in cuisines]
    )
