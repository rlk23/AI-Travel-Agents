import requests
import json
from datetime import datetime
from database.crud import user
from database.models import Passenger, Booking, BookingItem
from sqlalchemy.orm import Session
import uuid

class FlightBookingAgent:
    def __init__(self, access_token, db: Session = None):
        self.access_token = access_token
        self.booking_endpoint = "https://test.api.amadeus.com/v1/booking/flight-orders"
        self.db = db

    def create_booking(self, flight_offer, traveler_info, contact_info):
        """
        Create a flight booking using the Amadeus API.
        
        Args:
            flight_offer (dict): The selected flight offer from search results
            traveler_info (dict): Information about the traveler(s)
            contact_info (dict): Contact information for the booking
            
        Returns:
            dict: Booking confirmation or error message
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # Prepare the booking payload
        payload = {
            "data": {
                "type": "flight-order",
                "flightOffers": [flight_offer],
                "travelers": self._prepare_travelers(traveler_info),
                "remarks": {
                    "general": [
                        {
                            "subType": "GENERAL_MISCELLANEOUS",
                            "text": "Booking created via AI Travel Agent"
                        }
                    ]
                },
                "ticketingAgreement": {
                    "option": "DELAY_TO_CANCEL",
                    "delay": "6D"
                },
                "contacts": [
                    {
                        "addresseeName": {
                            "firstName": contact_info.get("firstName", ""),
                            "lastName": contact_info.get("lastName", "")
                        },
                        "companyName": contact_info.get("companyName", ""),
                        "purpose": "STANDARD",
                        "phones": [
                            {
                                "deviceType": "MOBILE",
                                "countryCallingCode": contact_info.get("countryCallingCode", "1"),
                                "number": contact_info.get("phoneNumber", "")
                            }
                        ],
                        "emailAddress": contact_info.get("email", ""),
                        "address": {
                            "lines": contact_info.get("addressLines", []),
                            "postalCode": contact_info.get("postalCode", ""),
                            "cityName": contact_info.get("city", ""),
                            "countryCode": contact_info.get("countryCode", "US")
                        }
                    }
                ]
            }
        }

        try:
            response = requests.post(self.booking_endpoint, headers=headers, json=payload)
            
            if response.status_code == 201:
                booking_data = response.json()
                return {
                    "status": "success",
                    "booking_id": booking_data["data"]["id"],
                    "booking_reference": booking_data["data"]["bookingReference"],
                    "details": booking_data["data"]
                }
            else:
                error_data = response.json()
                return {
                    "status": "error",
                    "error": error_data.get("errors", [{"detail": "Unknown error occurred"}])[0]["detail"]
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def _prepare_travelers(self, traveler_info):
        """
        Prepare traveler information in the format required by the Amadeus API.
        """
        travelers = []
        for traveler in traveler_info:
            traveler_data = {
                "id": traveler.get("id", "1"),
                "dateOfBirth": traveler.get("dateOfBirth", ""),
                "name": {
                    "firstName": traveler.get("firstName", ""),
                    "lastName": traveler.get("lastName", "")
                },
                "gender": traveler.get("gender", "MALE"),
                "contact": {
                    "emailAddress": traveler.get("email", ""),
                    "phones": [
                        {
                            "deviceType": "MOBILE",
                            "countryCallingCode": traveler.get("countryCallingCode", "1"),
                            "number": traveler.get("phoneNumber", "")
                        }
                    ]
                },
                "documents": [
                    {
                        "documentType": "PASSPORT",
                        "birthPlace": traveler.get("birthPlace", ""),
                        "issuanceLocation": traveler.get("issuanceLocation", ""),
                        "issuanceDate": traveler.get("issuanceDate", ""),
                        "number": traveler.get("passportNumber", ""),
                        "expiryDate": traveler.get("passportExpiryDate", ""),
                        "issuanceCountry": traveler.get("issuanceCountry", "US"),
                        "validityCountry": traveler.get("validityCountry", "US"),
                        "nationality": traveler.get("nationality", "US"),
                        "holder": True
                    }
                ]
            }
            travelers.append(traveler_data)
        return travelers

    def get_booking_status(self, booking_id):
        """
        Retrieve the status of a flight booking.
        
        Args:
            booking_id (str): The ID of the booking to check
            
        Returns:
            dict: Booking status information
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.get(
                f"{self.booking_endpoint}/{booking_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "booking_status": response.json()
                }
            else:
                error_data = response.json()
                return {
                    "status": "error",
                    "error": error_data.get("errors", [{"detail": "Unknown error occurred"}])[0]["detail"]
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def cancel_booking(self, booking_id):
        """
        Cancel a flight booking.
        
        Args:
            booking_id (str): The ID of the booking to cancel
            
        Returns:
            dict: Cancellation status
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.delete(
                f"{self.booking_endpoint}/{booking_id}",
                headers=headers
            )
            
            if response.status_code == 204:
                return {
                    "status": "success",
                    "message": "Booking cancelled successfully"
                }
            else:
                error_data = response.json()
                return {
                    "status": "error",
                    "error": error_data.get("errors", [{"detail": "Unknown error occurred"}])[0]["detail"]
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def create_booking_with_db(self, flight_offer, user_id, traveler_info, contact_info):
        """
        Create a flight booking and store it in the database.
        
        Args:
            flight_offer (dict): The selected flight offer from search results
            user_id (UUID): The ID of the user making the booking
            traveler_info (list): List of traveler information dictionaries
            contact_info (dict): Contact information for the booking
            
        Returns:
            dict: Booking confirmation or error message
        """
        if not self.db:
            return {"status": "error", "error": "Database session not initialized"}

        try:
            # Create the booking with Amadeus API
            booking_result = self.create_booking(flight_offer, traveler_info, contact_info)
            
            if booking_result["status"] != "success":
                return booking_result

            # Create database booking record
            db_booking = Booking(
                user_id=user_id,
                booking_reference=booking_result["booking_reference"],
                booking_status="CONFIRMED",
                total_price=float(flight_offer["price"]["total"]),
                currency=flight_offer["price"]["currency"],
                payment_status="PAID"
            )
            self.db.add(db_booking)
            self.db.flush()  # Get the booking_id

            # Create booking item
            booking_item = BookingItem(
                booking_id=db_booking.booking_id,
                item_type="FLIGHT",
                item_reference_id=uuid.UUID(flight_offer["id"]),
                quantity=len(traveler_info),
                unit_price=float(flight_offer["price"]["total"]) / len(traveler_info),
                total_price=float(flight_offer["price"]["total"]),
                currency=flight_offer["price"]["currency"],
                booking_status="CONFIRMED",
                supplier_reference=booking_result["booking_reference"]
            )
            self.db.add(booking_item)

            # Create passenger records
            for traveler in traveler_info:
                passenger = Passenger(
                    booking_id=db_booking.booking_id,
                    first_name=traveler["firstName"],
                    last_name=traveler["lastName"],
                    date_of_birth=datetime.strptime(traveler["dateOfBirth"], "%Y-%m-%d").date(),
                    nationality=traveler.get("nationality", "US"),
                    passport_number=traveler.get("passportNumber", ""),
                    passport_expiry=datetime.strptime(traveler.get("passportExpiryDate", "2099-12-31"), "%Y-%m-%d").date(),
                    special_requests=traveler.get("specialRequests", "")
                )
                self.db.add(passenger)

            self.db.commit()

            return {
                "status": "success",
                "booking_id": str(db_booking.booking_id),
                "booking_reference": booking_result["booking_reference"],
                "details": booking_result["details"]
            }

        except Exception as e:
            self.db.rollback()
            return {
                "status": "error",
                "error": str(e)
            }
