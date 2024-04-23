from db.base import async_session_maker
from db.models import (UserModel, SessionModel, AttractionModel, AttractionTicketModel, EventTicketModel,
                       EventModel, RestaurantModel, TagModel, AttractionTagModel, LocationModel, AgeModel,
                       AttractionAgeModel, RestaurantCuisineModel, RestaurantPhotoModel, CuisineModel,
                       AttractionReviewModel, RestaurantTableBookingModel)
from db.services.base_service import BaseService


class UserService(BaseService[UserModel]):
    model = UserModel
    session_maker = async_session_maker


class SessionService(BaseService[SessionModel]):
    model = SessionModel
    session_maker = async_session_maker


class AttractionService(BaseService[AttractionModel]):
    model = AttractionModel
    session_maker = async_session_maker


class TagService(BaseService[TagModel]):
    model = TagModel
    session_maker = async_session_maker


class AttractionTagService(BaseService[AttractionTagModel]):
    model = AttractionTagModel
    session_maker = async_session_maker


class AgeService(BaseService[AttractionModel]):
    model = AgeModel
    session_maker = async_session_maker


class AttractionAgeService(BaseService[AttractionAgeModel]):
    model = AttractionAgeModel
    session_maker = async_session_maker


class LocationService(BaseService[LocationModel]):
    model = LocationModel
    session_maker = async_session_maker


class AttractionTicketService(BaseService[AttractionTicketModel]):
    model = AttractionTicketModel
    session_maker = async_session_maker


class EventService(BaseService[EventModel]):
    model = EventModel
    session_maker = async_session_maker


class EventTicketService(BaseService[EventTicketModel]):
    model = EventTicketModel
    session_maker = async_session_maker


class RestaurantService(BaseService[RestaurantModel]):
    model = RestaurantModel
    session_maker = async_session_maker


class RestaurantCuisineService(BaseService[RestaurantCuisineModel]):
    model = RestaurantCuisineModel
    session_maker = async_session_maker


class RestaurantPhotoService(BaseService[RestaurantPhotoModel]):
    model = RestaurantPhotoModel
    session_maker = async_session_maker


class CuisineService(BaseService[CuisineModel]):
    model = CuisineModel
    session_maker = async_session_maker


class AttractionReviewService(BaseService[AttractionReviewModel]):
    model = AttractionReviewModel
    session_maker = async_session_maker


class RestaurantTableBookingService(BaseService[RestaurantTableBookingModel]):
    model = RestaurantTableBookingModel
    session_maker = async_session_maker
