# flight_search_agent.py
import requests

class FlightSearchAgent:
    def __init__(self, access_token):
        self.access_token = access_token

    def search_flights(self, origin, destination, date):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": date,
            "adults": 1,
            "currencyCode": "USD",
            "max": 5
        }

        response = requests.get(
            "https://test.api.amadeus.com/v2/shopping/flight-offers",
            headers=headers,
            params=params
        )
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching flights:", response.json().get("errors", response.text))
            return {"error": "Failed to retrieve flights"}
