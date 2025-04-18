# database/models.py
import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, Date, Time, DateTime, ForeignKey, Text, JSON, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .config import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    date_of_birth = Column(Date)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    preferences = relationship("UserPreference", back_populates="user", cascade="all, delete-orphan")
    itineraries = relationship("Itinerary", back_populates="user")
    bookings = relationship("Booking", back_populates="user")


class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    preference_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    preference_type = Column(String(50), nullable=False)
    preference_key = Column(String(100), nullable=False)
    preference_value = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="preferences")
    
    # Unique constraint
    __table_args__ = (
        {'schema': 'public'},
    )


class Airline(Base):
    __tablename__ = "airlines"
    
    airline_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    iata_code = Column(String(2))
    icao_code = Column(String(3))
    logo_url = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relationships
    flights = relationship("Flight", back_populates="airline")


class Airport(Base):
    __tablename__ = "airports"
    
    airport_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    iata_code = Column(String(3))
    icao_code = Column(String(4))
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))
    timezone = Column(String(50))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relationships
    departures = relationship("Flight", foreign_keys="Flight.departure_airport_id", back_populates="departure_airport")
    arrivals = relationship("Flight", foreign_keys="Flight.arrival_airport_id", back_populates="arrival_airport")


class Flight(Base):
    __tablename__ = "flights"
    
    flight_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flight_number = Column(String(10), nullable=False)
    airline_id = Column(UUID(as_uuid=True), ForeignKey("airlines.airline_id"))
    departure_airport_id = Column(UUID(as_uuid=True), ForeignKey("airports.airport_id"))
    arrival_airport_id = Column(UUID(as_uuid=True), ForeignKey("airports.airport_id"))
    departure_time = Column(TIMESTAMP(timezone=True), nullable=False)
    arrival_time = Column(TIMESTAMP(timezone=True), nullable=False)
    aircraft_type = Column(String(50))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    airline = relationship("Airline", back_populates="flights")
    departure_airport = relationship("Airport", foreign_keys=[departure_airport_id], back_populates="departures")
    arrival_airport = relationship("Airport", foreign_keys=[arrival_airport_id], back_populates="arrivals")
    prices = relationship("FlightPrice", back_populates="flight", cascade="all, delete-orphan")


class FlightPrice(Base):
    __tablename__ = "flight_prices"
    
    price_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flight_id = Column(UUID(as_uuid=True), ForeignKey("flights.flight_id", ondelete="CASCADE"), nullable=False)
    cabin_class = Column(String(20), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), server_default="USD")
    availability = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    flight = relationship("Flight", back_populates="prices")


class HotelChain(Base):
    __tablename__ = "hotel_chains"
    
    chain_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    website = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relationships
    hotels = relationship("Hotel", back_populates="chain")


class Hotel(Base):
    __tablename__ = "hotels"
    
    hotel_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chain_id = Column(UUID(as_uuid=True), ForeignKey("hotel_chains.chain_id"))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    postal_code = Column(String(20))
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))
    star_rating = Column(DECIMAL(2, 1))
    amenities = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    chain = relationship("HotelChain", back_populates="hotels")
    room_types = relationship("RoomType", back_populates="hotel", cascade="all, delete-orphan")


class RoomType(Base):
    __tablename__ = "room_types"
    
    room_type_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id = Column(UUID(as_uuid=True), ForeignKey("hotels.hotel_id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    max_occupancy = Column(Integer, nullable=False)
    amenities = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relationships
    hotel = relationship("Hotel", back_populates="room_types")
    availability = relationship("RoomAvailability", back_populates="room_type", cascade="all, delete-orphan")


class RoomAvailability(Base):
    __tablename__ = "room_availability"
    
    availability_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_type_id = Column(UUID(as_uuid=True), ForeignKey("room_types.room_type_id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    available_rooms = Column(Integer, nullable=False)
    price_per_night = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), server_default="USD")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    room_type = relationship("RoomType", back_populates="availability")
    
    # Unique constraint
    __table_args__ = (
        {'schema': 'public'},
    )


class ActivityCategory(Base):
    __tablename__ = "activity_categories"
    
    category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relationships
    activities = relationship("Activity", back_populates="category")


class Activity(Base):
    __tablename__ = "activities"
    
    activity_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("activity_categories.category_id"))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    location = Column(String(255))
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))
    duration_minutes = Column(Integer)
    min_participants = Column(Integer, server_default="1")
    max_participants = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    category = relationship("ActivityCategory", back_populates="activities")
    availability = relationship("ActivityAvailability", back_populates="activity", cascade="all, delete-orphan")


class ActivityAvailability(Base):
    __tablename__ = "activity_availability"
    
    availability_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("activities.activity_id", ondelete="CASCADE"), nullable=False)
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    available_spots = Column(Integer, nullable=False)
    price_per_person = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), server_default="USD")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    activity = relationship("Activity", back_populates="availability")


class Itinerary(Base):
    __tablename__ = "itineraries"
    
    itinerary_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    title = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    destination_city = Column(String(100))
    destination_country = Column(String(100))
    is_ai_generated = Column(Boolean, server_default="false")
    status = Column(String(20), server_default="draft")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="itineraries")
    items = relationship("ItineraryItem", back_populates="itinerary", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="itinerary")


class ItineraryItem(Base):
    __tablename__ = "itinerary_items"
    
    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itinerary_id = Column(UUID(as_uuid=True), ForeignKey("itineraries.itinerary_id", ondelete="CASCADE"), nullable=False)
    item_type = Column(String(20), nullable=False)
    item_reference_id = Column(UUID(as_uuid=True))
    day_number = Column(Integer, nullable=False)
    start_time = Column(TIMESTAMP(timezone=True))
    end_time = Column(TIMESTAMP(timezone=True))
    title = Column(String(100), nullable=False)
    description = Column(Text)
    location = Column(String(255))
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))
    notes = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    itinerary = relationship("Itinerary", back_populates="items")


class Booking(Base):
    __tablename__ = "bookings"
    
    booking_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    itinerary_id = Column(UUID(as_uuid=True), ForeignKey("itineraries.itinerary_id"))
    booking_reference = Column(String(50), unique=True)
    booking_status = Column(String(20), nullable=False)
    total_price = Column(DECIMAL(12, 2), nullable=False)
    currency = Column(String(3), server_default="USD")
    payment_status = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    itinerary = relationship("Itinerary", back_populates="bookings")
    items = relationship("BookingItem", back_populates="booking", cascade="all, delete-orphan")
    passengers = relationship("Passenger", back_populates="booking", cascade="all, delete-orphan")


class BookingItem(Base):
    __tablename__ = "booking_items"
    
    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.booking_id", ondelete="CASCADE"), nullable=False)
    item_type = Column(String(20), nullable=False)
    item_reference_id = Column(UUID(as_uuid=True), nullable=False)
    quantity = Column(Integer, server_default="1")
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), server_default="USD")
    booking_status = Column(String(20), nullable=False)
    supplier_reference = Column(String(100))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    booking = relationship("Booking", back_populates="items")


class Passenger(Base):
    __tablename__ = "passengers"
    
    passenger_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.booking_id", ondelete="CASCADE"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    nationality = Column(String(100))
    passport_number = Column(String(50))
    passport_expiry = Column(Date)
    special_requests = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relationships
    booking = relationship("Booking", back_populates="passengers")


class UserBehavior(Base):
    __tablename__ = "user_behavior"
    
    behavior_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    interaction_type = Column(String(50), nullable=False)
    item_type = Column(String(20))
    item_id = Column(UUID(as_uuid=True))
    context = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"
    
    recommendation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    recommendation_type = Column(String(50), nullable=False)
    item_id = Column(UUID(as_uuid=True))
    rank = Column(Integer, nullable=False)
    confidence_score = Column(DECIMAL(5, 4))
    reasoning = Column(Text)
    is_shown = Column(Boolean, server_default="false")
    is_clicked = Column(Boolean, server_default="false")
    is_booked = Column(Boolean, server_default="false")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"
    
    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)
    related_item_type = Column(String(20))
    related_item_id = Column(UUID(as_uuid=True))
    is_read = Column(Boolean, server_default="false")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())