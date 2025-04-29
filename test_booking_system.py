import requests
import json
import uuid
from datetime import datetime, timedelta

# Test configuration
BASE_URL = "http://localhost:5002"
TEST_USER_ID = str(uuid.uuid4())  # Generate a test user ID

def test_flight_search():
    """Test the flight search functionality"""
    print("\n=== Testing Flight Search ===")
    try:
        response = requests.post(
            f"{BASE_URL}/api/ai-agent",
            json={
                "prompt": "I want to fly from New York to London on 2024-06-01"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Flight search successful!")
            print("Found flights:", len(data.get("departure_flights", [])))
            return data.get("departure_flights", [])
        else:
            print("❌ Flight search failed!")
            print("Status code:", response.status_code)
            print("Response:", response.text)
            return None
    except Exception as e:
        print("❌ Error during flight search:", str(e))
        return None

def test_booking(flight_offer):
    """Test the booking functionality"""
    if not flight_offer:
        print("❌ No flight offer available for booking test")
        return None

    print("\n=== Testing Flight Booking ===")
    try:
        # Prepare booking data
        booking_data = {
            "user_id": TEST_USER_ID,
            "flight_offer": flight_offer,
            "traveler_info": [
                {
                    "firstName": "John",
                    "lastName": "Doe",
                    "dateOfBirth": "1990-01-01",
                    "nationality": "US",
                    "passportNumber": "AB123456",
                    "passportExpiryDate": "2025-01-01",
                    "specialRequests": "Window seat preferred"
                }
            ],
            "contact_info": {
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "phoneNumber": "1234567890",
                "countryCallingCode": "1",
                "addressLines": ["123 Main St"],
                "postalCode": "10001",
                "city": "New York",
                "countryCode": "US"
            }
        }

        response = requests.post(
            f"{BASE_URL}/api/book-flight",
            json=booking_data
        )

        if response.status_code == 201:
            data = response.json()
            print("✅ Booking successful!")
            print("Booking ID:", data.get("booking_id"))
            print("Booking Reference:", data.get("booking_reference"))
            return data.get("booking_id")
        else:
            print("❌ Booking failed!")
            print("Status code:", response.status_code)
            print("Response:", response.text)
            return None
    except Exception as e:
        print("❌ Error during booking:", str(e))
        return None

def test_booking_status(booking_id):
    """Test the booking status check"""
    if not booking_id:
        print("❌ No booking ID available for status check")
        return

    print("\n=== Testing Booking Status ===")
    try:
        response = requests.get(
            f"{BASE_URL}/api/booking-status/{booking_id}"
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Status check successful!")
            print("Booking Status:", data)
        else:
            print("❌ Status check failed!")
            print("Status code:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("❌ Error during status check:", str(e))

def test_cancel_booking(booking_id):
    """Test the booking cancellation"""
    if not booking_id:
        print("❌ No booking ID available for cancellation")
        return

    print("\n=== Testing Booking Cancellation ===")
    try:
        response = requests.delete(
            f"{BASE_URL}/api/cancel-booking/{booking_id}"
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Cancellation successful!")
            print("Response:", data)
        else:
            print("❌ Cancellation failed!")
            print("Status code:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("❌ Error during cancellation:", str(e))

def main():
    """Run all tests"""
    print("Starting AI Travel Agent System Tests...")
    
    # Test flight search
    flights = test_flight_search()
    
    if flights:
        # Test booking with first available flight
        booking_id = test_booking(flights[0])
        
        if booking_id:
            # Test booking status
            test_booking_status(booking_id)
            
            # Test cancellation (uncomment to test cancellation)
            # test_cancel_booking(booking_id)

if __name__ == "__main__":
    main() 