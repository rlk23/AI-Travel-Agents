# city_to_airport_agent.py
import requests
import time
#from config import FLIGHT_API_KEY, FLIGHT_API_SECRET
from load_environement import flight_api_key, flight_api_secret

class CityToAirportAgent:
    def __init__(self):
        self.access_token = self.authenticate()

    def authenticate(self):
        response = requests.post(
            "https://test.api.amadeus.com/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": flight_api_key,
                "client_secret": flight_api_secret
            }
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception("Failed to authenticate with Amadeus API: " + response.text)

    def city_to_airport_code(self, city_name, max_retries=3):
        if not city_name or not city_name.strip():
            print(f"Invalid city name provided: '{city_name}'")
            return None

        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "subType": "AIRPORT,CITY",
            "keyword": city_name.strip(),
            "page[limit]": 1
        }

        for attempt in range(max_retries):
            response = requests.get(
                "https://test.api.amadeus.com/v1/reference-data/locations",
                headers=headers,
                params=params
            )
            if response.status_code == 200:
                data = response.json()
                if "data" in data and data["data"]:
                    return data["data"][0]["iataCode"]
                else:
                    print(f"No airport or city found for '{city_name}'")
                    return None
            elif response.status_code == 429:
                print("Rate limit exceeded. Retrying...")
                time.sleep(5)
            else:
                print("Error fetching airport code:", response.json().get("errors", response.text))
                return None

        print(f"Failed to retrieve airport code for '{city_name}' after {max_retries} attempts.")
        return None
