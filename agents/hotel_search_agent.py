import requests


class HotelSearchAgent:
    def __init__(self, access_token):
        self.accces_token = access_token

    

    def search_hotels(self,city, check_in, check_out, max_results=5):
        headers = {"Authorization":f"Bearer {self.access_token}"}

        params = {
            "cityCode": city,
            "checkInDate": check_in,
            "checkOutDate": check_out,
            "adults": 1,
            "roomQuantity": 1,
            "max": max_results
        }

        response = requests.get(
            "https://test.api.amadeus.com/v2/shopping/hotel-offers",
            headers=headers,
            params=params
        )


        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching hotels:", response.json().get("errors",response.text))
            return {"error":"Failed to retrieve hotels"}
    


    def book_hotel(self, hotel_id, room_id, guests, payment_details):

        headers = {"Authorization":f"Bearer {self.access_token}"}
        payload = {
            "hotelsId": hotel_id,
            "roomId":room_id,
            "guests": guests,
            "paymentDetails": payment_details
        }

        
        response = requests.post(
            "https://test.api.amadeus.com/v2/booking/hotel-bookings",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            return response.json()
        
        else:
            print("Error booking hotel:", response.json().get("errors", response.text))
            return {"error": "Failed to book hotel"}
        

