from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, CheckConstraint, Boolean, Date, \
    UniqueConstraint, Time, Text
from sqlalchemy.orm import relationship, Mapped

from db.base import Base

metadata = Base.metadata


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    password = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone = Column(String(255))

    def __repr__(self) -> str:
        return (
            f'UserModel(id={self.id}, name={self.email})'
        )


class SessionModel(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    #user: Mapped["UserModel"] = relationship('UserModel')
    access_token = Column(String(255), nullable=True)
    expires_at = Column(DateTime)

    def __repr__(self) -> str:
        return (
            f'SessionModel(id={self.id}, user_id={self.user_id})'
        )


class AttractionModel(Base):
    __tablename__ = "attraction"

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    price = Column(Integer, CheckConstraint('price >= 0'), nullable=True)
    duration = Column(Integer, CheckConstraint('duration > 0'), nullable=True)
    minimum_height = Column(Float, CheckConstraint('minimum_height > 0'), nullable=True)
    photo_url = Column(String(255), nullable=True)


class LocationModel(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class AttractionTicketModel(Base):
    __tablename__ = 'attraction_ticket'
    id = Column(Integer, primary_key=True)
    attraction_id = Column(Integer, ForeignKey('attraction.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    is_expired = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)


class EventModel(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    price = Column(Integer, nullable=False)
    photo_url = Column(String(255), nullable=False)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    __table_args__ = (CheckConstraint('start_at < end_at', name='chk_time'),)


class EventTicketModel(Base):
    __tablename__ = 'event_ticket'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    is_expired = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)


class AttractionReviewModel(Base):
    __tablename__ = 'attraction_review'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    attraction_id = Column(Integer, ForeignKey('attraction.id'), nullable=False)
    description = Column(String(1000))
    created_at = Column(Date, nullable=False)
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'))


class TagModel(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)


class AttractionTagModel(Base):
    __tablename__ = 'attraction_tag'
    id = Column(Integer, primary_key=True)
    attraction_id = Column(Integer, ForeignKey('attraction.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)
    __table_args__ = (UniqueConstraint('attraction_id', 'tag_id'),)


class AgeModel(Base):
    __tablename__ = 'age'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)


class AttractionAgeModel(Base):
    __tablename__ = 'attraction_age'
    id = Column(Integer, primary_key=True)
    attraction_id = Column(Integer, ForeignKey('attraction.id'), nullable=False)
    age_id = Column(Integer, ForeignKey('age.id'), nullable=False)
    __table_args__ = (UniqueConstraint('attraction_id', 'age_id'),)


class CuisineModel(Base):
    __tablename__ = 'cuisine'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)


class RestaurantModel(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(50))
    description = Column(String)
    location_id = Column(Integer, ForeignKey('location.id'))
    open_at = Column(Time, nullable=False)
    close_at = Column(Time, nullable=False)
    menu_url = Column(String(255))
    __table_args__ = (CheckConstraint('open_at < close_at', name='chk_times'),)


class RestaurantPhotoModel(Base):
    __tablename__ = 'restaurant_photo'
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'), nullable=False)
    url = Column(String(255), nullable=False)


class RestaurantCuisineModel(Base):
    __tablename__ = 'restaurant_cuisine'
    id = Column(Integer, primary_key=True)
    cuisine_id = Column(Integer, ForeignKey('cuisine.id'), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'), nullable=False)
    __table_args__ = (UniqueConstraint('cuisine_id', 'restaurant_id'),)


class RestaurantTableModel(Base):
    __tablename__ = 'restaurant_table'
    id = Column(Integer, primary_key=True)
    capacity = Column(Integer, CheckConstraint('capacity > 0'))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'), nullable=False)


class RestaurantTableBookingModel(Base):
    __tablename__ = 'restaurant_table_booking'
    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey('restaurant_table.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    date_time = Column(DateTime, nullable=False)


class LoggingModel(Base):
    __tablename__ = 'logging'

    id = Column(Integer, primary_key=True)
    role = Column(String(255), nullable=False)
    log_time = Column(DateTime, default=datetime.utcnow())
    action_text = Column(Text, nullable=False)