import requests
import time
from typing import Optional

class CityToAirportAgent:
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize the CityToAirportAgent with Amadeus API credentials.
        
        Args:
            api_key (str): Amadeus API key
            api_secret (str): Amadeus API secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://test.api.amadeus.com"
        self.access_token = self.authenticate()

    def authenticate(self) -> str:
        """
        Authenticate with Amadeus API to get access token.
        
        Returns:
            str: Access token if successful, raises exception otherwise
        """
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/security/oauth2/token", 
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["access_token"]
            else:
                print(f"Authentication failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                raise Exception(f"Failed to authenticate with Amadeus API: {response.text}")
        except requests.RequestException as e:
            print(f"Request exception during authentication: {str(e)}")
            raise Exception(f"Authentication request failed: {str(e)}")

    def refresh_token_if_needed(self) -> None:
        """Refresh the access token if needed"""
        try:
            # Test the token with a simple request
            headers = {"Authorization": f"Bearer {self.access_token}"}
            test_response = requests.get(
                f"{self.base_url}/v1/reference-data/locations",
                headers=headers,
                params={"keyword": "LON", "subType": "CITY", "page[limit]": 1},
                timeout=10
            )
            
            # If unauthorized, refresh the token
            if test_response.status_code == 401:
                print("Access token expired. Refreshing...")
                self.access_token = self.authenticate()
                print("Token refreshed successfully")
                
        except Exception as e:
            print(f"Error testing token validity: {str(e)}")
            # Refresh token as a precaution
            self.access_token = self.authenticate()

    def city_to_airport_code(self, city_name: str, max_retries: int = 3) -> Optional[str]:
        """
        Convert city name to airport code using Amadeus API.
        
        Args:
            city_name (str): Name of the city
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            Optional[str]: IATA code if found, None otherwise
        """
        if not city_name or not isinstance(city_name, str) or not city_name.strip():
            print(f"Invalid city name provided: '{city_name}'")
            return None

        # Ensure we have a valid token
        self.refresh_token_if_needed()
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "subType": "AIRPORT,CITY",
            "keyword": city_name.strip(),
            "page[limit]": 5  # Increased to get more options
        }

        for attempt in range(max_retries):
            try:
                response = requests.get(
                    f"{self.base_url}/v1/reference-data/locations",
                    headers=headers,
                    params=params,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "data" in data and data["data"]:
                        # First try to find exact match for the city
                        for location in data["data"]:
                            if location.get("subType") == "CITY" and location.get("name", "").lower() == city_name.lower():
                                return location["iataCode"]
                        
                        # If no exact city match, return the first airport or city code
                        return data["data"][0]["iataCode"]
                    else:
                        print(f"No airport or city found for '{city_name}'")
                        return None
                elif response.status_code == 401:
                    # Unauthorized - refresh token and retry
                    print("Token expired during request. Refreshing...")
                    self.access_token = self.authenticate()
                    continue
                elif response.status_code == 429:
                    # Rate limit - wait and retry
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Rate limit exceeded. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    print(f"Error fetching airport code (Status {response.status_code}):", 
                          response.json().get("errors", response.text))
                    if attempt < max_retries - 1:
                        time.sleep(1)  # Brief pause before retry
                    else:
                        return None
                        
            except requests.Timeout:
                print(f"Request timed out on attempt {attempt + 1}/{max_retries}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    return None
            except Exception as e:
                print(f"Unexpected error on attempt {attempt + 1}/{max_retries}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    return None

        print(f"Failed to retrieve airport code for '{city_name}' after {max_retries} attempts.")
        return None