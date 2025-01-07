import requests

class FlightSearchAgent:
    def __init__(self, access_token):
        self.access_token = access_token

    def search_flights(self, origin, destination, date, cabin="ECONOMY", time="00:00:00", max_offers=5):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "currencyCode": "USD",
            "originDestinations": [
                {
                    "id": "1",
                    "originLocationCode": origin,
                    "destinationLocationCode": destination,
                    "departureDateTimeRange": {
                        "date": date,
                        "time": time
                    }
                }
            ],
            "travelers": [
                {
                    "id": "1",
                    "travelerType": "ADULT"
                }
            ],
            "sources": ["GDS"],
            "searchCriteria": {
                "maxFlightOffers": max_offers,
                "flightFilters": {
                    "cabinRestrictions": [
                        {
                            "cabin": cabin.upper(),
                            "coverage": "MOST_SEGMENTS",
                            "originDestinationIds": ["1"]
                        }
                    ]
                }
            }
        }

        response = requests.post(
            "https://test.api.amadeus.com/v2/shopping/flight-offers",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching flights:", response.json().get("errors", response.text))
            return {"error": "Failed to retrieve flights"}