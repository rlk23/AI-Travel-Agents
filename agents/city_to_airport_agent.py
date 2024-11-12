import requests
from config import FLIGHT_API_KEY, FLIGHT_API_SECRET

class CityToAirportAgent:
    def __init__(self):
        # Authenticate and obtain an access token for the Amadeus API
        self.access_token = self.authenticate()

    def authenticate(self):
        """Authenticate with the Amadeus API and retrieve an access token."""
        response = requests.post(
            "https://test.api.amadeus.com/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": FLIGHT_API_KEY,
                "client_secret": FLIGHT_API_SECRET
            }
        )
        # Ensure authentication was successful
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception("Failed to authenticate with Amadeus API: " + response.text)

    def city_to_airport_code(self, city_name):
        """
        Retrieve the primary airport code for a given city.
        
        Args:
            city_name (str): The name of the city.

        Returns:
            str: The IATA code for the primary airport in the city.
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "subType": "AIRPORT",
            "keyword": city_name,
            "page[limit]": 1
        }
        
        response = requests.get(
            "https://test.api.amadeus.com/v1/reference-data/locations",
            headers=headers,
            params=params
        )
        
        # Check for successful response
        if response.status_code == 200:
            data = response.json()
            if data["data"]:
                return data["data"][0]["iataCode"]  # Return the first airport code found
            else:
                print(f"No airport found for city '{city_name}'")
                return None
        else:
            print("Error fetching airport code:", response.json().get("error", response.text))
            return None
