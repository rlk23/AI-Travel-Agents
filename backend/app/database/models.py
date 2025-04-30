from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .base import Base

class Flight(Base):
    __tablename__ = "flights"

    flight_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    airline = Column(String, nullable=False)
    flight_number = Column(String, nullable=False)
    departure_airport = Column(String, nullable=False)
    arrival_airport = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    available_seats = Column(Integer, nullable=False)
    aircraft_type = Column(String)
    duration = Column(Integer)  # in minutes
    stops = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bookings = relationship("FlightBooking", back_populates="flight")

class FlightBooking(Base):
    __tablename__ = "flight_bookings"

    booking_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flight_id = Column(UUID(as_uuid=True), ForeignKey("flights.flight_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    booking_reference = Column(String, unique=True, nullable=False)
    passenger_count = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    booking_status = Column(String, nullable=False)  # e.g., "confirmed", "cancelled", "pending"
    payment_status = Column(String, nullable=False)  # e.g., "paid", "pending", "refunded"
    passenger_details = Column(JSON)  # Store passenger information
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    flight = relationship("Flight", back_populates="bookings")
    user = relationship("User", back_populates="flight_bookings") 