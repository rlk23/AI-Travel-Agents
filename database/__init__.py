# database/__init__.py
from .config import engine, Base, get_db
from .models import (
    User, UserPreference, Airline, Airport, Flight, FlightPrice, 
    HotelChain, Hotel, RoomType, RoomAvailability,
    ActivityCategory, Activity, ActivityAvailability,
    Itinerary, ItineraryItem, Booking, BookingItem, Passenger,
    UserBehavior, AIRecommendation, Notification
)
from .init_db import init_db
from .crud import user

# Export all models and utilities
__all__ = [
    'engine', 'Base', 'get_db', 'init_db',
    'User', 'UserPreference', 'Airline', 'Airport', 'Flight', 'FlightPrice',
    'HotelChain', 'Hotel', 'RoomType', 'RoomAvailability',
    'ActivityCategory', 'Activity', 'ActivityAvailability',
    'Itinerary', 'ItineraryItem', 'Booking', 'BookingItem', 'Passenger',
    'UserBehavior', 'AIRecommendation', 'Notification',
    'user'  # CRUD utility for User model
]

# Example of updating your main.py to initialize the database
"""
To initialize the database when starting your application, add this to your main.py:

from database import init_db

# Initialize database tables
init_db()

# Rest of your application code
"""