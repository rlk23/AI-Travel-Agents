import requests

class HotelSearchAgent:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://test.api.amadeus.com"

    def get_city_code(self, airport_code):
        """
        Get the city code for a given airport code.
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{self.base_url}/v1/reference-data/locations"
        
        response = requests.get(
            url,
            headers=headers,
            params={
                "subType": "CITY",
                "keyword": airport_code,
                "page[limit]": 1
            }
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("data") and len(data["data"]) > 0:
                return data["data"][0]["iataCode"]
        return None

    def get_hotel_ids(self, city_code, limit=50):
        """
        Fetch hotel IDs for a given city code using the Amadeus API, limited to a specified number.
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{self.base_url}/v1/reference-data/locations/hotels/by-city"

        response = requests.get(
            url,
            headers=headers,
            params={"cityCode": city_code}
        )

        if response.status_code == 200:
            hotels = response.json().get('data', [])
            hotel_ids = [hotel['hotelId'] for hotel in hotels[:limit]]
            print(f"Fetched up to {limit} hotel IDs for city {city_code}: {hotel_ids}")
            return hotel_ids
        else:
            print(f"Error fetching hotel IDs for {city_code}: {response.json()}")
            return None

    def search_hotels(self, airport_code, check_in_date, check_out_date, adults=1):
        """
        Search for hotel offers using a limited number of hotel IDs.
        First converts airport code to city code, then searches for hotels.
        """
        # First get the city code from the airport code
        city_code = self.get_city_code(airport_code)
        if not city_code:
            return {"error": f"Could not find city code for airport {airport_code}"}

        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Fetch limited hotel IDs for the city
        hotel_ids = self.get_hotel_ids(city_code, limit=50)  # Limit to 50 hotels
        if not hotel_ids:
            print("No hotel IDs found for the specified city.")
            return {"error": "No hotels available in this city."}

        # Prepare a single request for the first 50 hotels
        url = f"{self.base_url}/v3/shopping/hotel-offers"
        params = {
            "hotelIds": ','.join(hotel_ids),
            "checkInDate": check_in_date,
            "checkOutDate": check_out_date,
            "adults": adults,
            "bestRateOnly": True
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            offers = response.json().get('data', [])
            if offers:
                return {"data": offers}
            else:
                return {"error": "No hotel offers available for the selected parameters."}
        else:
            print(f"Error fetching hotel offers: {response.json()}")
            return {"error": response.json()}
