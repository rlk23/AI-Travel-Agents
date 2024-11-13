import requests
import time
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
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception("Failed to authenticate with Amadeus API: " + response.text)

    def city_to_airport_code(self, city_name, max_retries=3):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "subType": "AIRPORT",
            "keyword": city_name,
            "page[limit]": 1
        }

        for attempt in range(max_retries):
            response = requests.get(
                "https://test.api.amadeus.com/v1/reference-data/locations",
                headers=headers,
                params=params
            )
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                if data["data"]:
                    return data["data"][0]["iataCode"]
                else:
                    print(f"No airport found for city '{city_name}'")
                    return None
            elif response.status_code == 429:
                print("Rate limit exceeded. Retrying after a short delay...")
                time.sleep(5)  # Wait 5 seconds before retrying
            else:
                print("Error fetching airport code:", response.json().get("error", response.text))
                return None

        print(f"Failed to retrieve airport code for '{city_name}' after {max_retries} attempts.")
        return None
