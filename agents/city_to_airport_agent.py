import requests
from config import FLIGHT_API_KEY, FLIGHT_API_SECRET

class CityToAirportAgent:
    def __init__(self):
        self.access_token = self.authenticate()

    
    def authenticate(self):
        response = requests.post(
            "https://test.api.amadeus.com/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": FLIGHT_API_KEY,
                "client_secret": FLIGHT_API_SECRET
            }
        )
        return response.json()["access_token"]
    
    def city_to_airport_code(self, city_name):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(
            f"https://test.api.amadeus.com/v1/reference-data/locations?subType=CITY&keyword={city_name}",
            headers=headers
        )
        data = response.json()
        return data["data"][0]["iataCode"] if data["data"] else None