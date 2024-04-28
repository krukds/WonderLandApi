from db.base import user_async_session_maker, manager_async_session_maker, admin_async_session_maker
from db.models import (UserModel, SessionModel, AttractionModel, AttractionTicketModel, EventTicketModel,
                       EventModel, RestaurantModel, TagModel, AttractionTagModel, LocationModel, AgeModel,
                       AttractionAgeModel, RestaurantCuisineModel, RestaurantPhotoModel, CuisineModel,
                       AttractionReviewModel, RestaurantTableBookingModel, LoggingModel)
from db.services.base_service import BaseService


class UserServiceForManager(BaseService[UserModel]):
    model = UserModel
    session_maker = manager_async_session_maker


class SessionServiceForManager(BaseService[SessionModel]):
    model = SessionModel
    session_maker = manager_async_session_maker


class SessionServiceForAdmin(BaseService[SessionModel]):
    model = SessionModel
    session_maker = admin_async_session_maker


class AttractionServiceForUser(BaseService[AttractionModel]):
    model = AttractionModel
    session_maker = user_async_session_maker


class AttractionServiceForManager(BaseService[AttractionModel]):
    model = AttractionModel
    session_maker = manager_async_session_maker


class TagServiceForUser(BaseService[TagModel]):
    model = TagModel
    session_maker = user_async_session_maker


class AttractionTagServiceForUser(BaseService[AttractionTagModel]):
    model = AttractionTagModel
    session_maker = user_async_session_maker


class AgeServiceForUser(BaseService[AttractionModel]):
    model = AgeModel
    session_maker = user_async_session_maker


class AttractionAgeServiceForUser(BaseService[AttractionAgeModel]):
    model = AttractionAgeModel
    session_maker = user_async_session_maker


class LocationServiceForUser(BaseService[LocationModel]):
    model = LocationModel
    session_maker = user_async_session_maker


class AttractionTicketServiceForUser(BaseService[AttractionTicketModel]):
    model = AttractionTicketModel
    session_maker = user_async_session_maker


class AttractionTicketServiceForAdmin(BaseService[AttractionTicketModel]):
    model = AttractionTicketModel
    session_maker = admin_async_session_maker


class EventServiceForUser(BaseService[EventModel]):
    model = EventModel
    session_maker = user_async_session_maker


class EventTicketServiceForUser(BaseService[EventTicketModel]):
    model = EventTicketModel
    session_maker = user_async_session_maker


class EventTicketServiceForAdmin(BaseService[EventTicketModel]):
    model = EventTicketModel
    session_maker = admin_async_session_maker



class RestaurantServiceForUser(BaseService[RestaurantModel]):
    model = RestaurantModel
    session_maker = user_async_session_maker


class RestaurantCuisineServiceForUser(BaseService[RestaurantCuisineModel]):
    model = RestaurantCuisineModel
    session_maker = user_async_session_maker


class RestaurantPhotoServiceForUser(BaseService[RestaurantPhotoModel]):
    model = RestaurantPhotoModel
    session_maker = user_async_session_maker


class CuisineServiceForUser(BaseService[CuisineModel]):
    model = CuisineModel
    session_maker = user_async_session_maker


class AttractionReviewServiceForUser(BaseService[AttractionReviewModel]):
    model = AttractionReviewModel
    session_maker = user_async_session_maker


class AttractionReviewServiceForAdmin(BaseService[AttractionReviewModel]):
    model = AttractionReviewModel
    session_maker = admin_async_session_maker



class RestaurantTableBookingServiceForUser(BaseService[RestaurantTableBookingModel]):
    model = RestaurantTableBookingModel
    session_maker = user_async_session_maker


class RestaurantTableBookingServiceForAdmin(BaseService[RestaurantTableBookingModel]):
    model = RestaurantTableBookingModel
    session_maker = admin_async_session_maker


class LoggingServiceForAdmin(BaseService[LoggingModel]):
    model = LoggingModel
    session_maker = admin_async_session_maker


