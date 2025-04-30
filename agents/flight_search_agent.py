import requests
import time
from typing import Dict

class FlightSearchAgent:
    def __init__(self, access_token: str):
        """
        Initialize the FlightSearchAgent with Amadeus API credentials.
        
        Args:
            access_token (str): Amadeus API access token
        """
        self.access_token = access_token
        self.base_url = "https://test.api.amadeus.com"
        self.airlines = {}  # Cache for airline names

    def search_flights(
        self,
        origin: str,
        destination: str,
        date: str,
        cabin: str = "ECONOMY",
        time: str = "00:00:00",
        max_offers: int = 5,
        passengers: int = 1
    ) -> Dict:
        """
        Search for flights using the Amadeus API.
        
        Args:
            origin (str): Departure airport IATA code
            destination (str): Arrival airport IATA code
            date (str): Departure date in YYYY-MM-DD format
            cabin (str): Cabin class (ECONOMY, BUSINESS, FIRST)
            time (str): Departure time in HH:MM:SS format
            max_offers (int): Maximum number of flight offers to return
            passengers (int): Number of passengers
            
        Returns:
            Dict: Processed flight search results or error message
        """
        # Validate inputs
        if not origin or not destination or not date:
            return {
                "status": "error",
                "error": "Origin, destination, and date are required"
            }
            
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
                    "id": str(i),
                    "travelerType": "ADULT"
                } for i in range(1, passengers + 1)
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

        try:
            print(f"Sending flight search request: {origin} to {destination} on {date}")
            response = requests.post(
                f"{self.base_url}/v2/shopping/flight-offers",
                headers=headers,
                json=payload,
                timeout=30
            )

            print(f"Flight search response status: {response.status_code}")
            
            if response.status_code == 200:
                results = self._process_flight_results(response.json())
                print(f"Found {len(results.get('flights', []))} flight results")
                return results
            elif response.status_code == 401:
                return {
                    "status": "error",
                    "error": "Authentication failed. Token may have expired."
                }
            else:
                try:
                    error_data = response.json()
                    error_detail = error_data.get("errors", [{"detail": "Unknown error occurred"}])[0]["detail"]
                    print(f"API error: {error_detail}")
                    return {
                        "status": "error",
                        "error": error_detail
                    }
                except:
                    return {
                        "status": "error",
                        "error": f"Error with status code {response.status_code}: {response.text}"
                    }
                
        except requests.Timeout:
            return {
                "status": "error",
                "error": "Request timed out. Please try again."
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "error": f"Request failed: {str(e)}"
            }
        except Exception as e:
            print(f"Unexpected error in search_flights: {str(e)}")
            return {
                "status": "error",
                "error": f"Unexpected error: {str(e)}"
            }

    def _process_flight_results(self, response_data: Dict) -> Dict:
        """
        Process and format the flight results from Amadeus API.
        
        Args:
            response_data (Dict): Raw response from Amadeus API
            
        Returns:
            Dict: Processed flight results
        """
        processed_flights = []
        
        for offer in response_data.get("data", []):
            flight = {
                "id": offer.get("id"),
                "price": {
                    "total": float(offer.get("price", {}).get("total", 0)),
                    "currency": offer.get("price", {}).get("currency", "USD"),
                    "base": float(offer.get("price", {}).get("base", 0)),
                    "fees": float(offer.get("price", {}).get("fees", 0)),
                    "taxes": float(offer.get("price", {}).get("taxes", 0))
                },
                "itineraries": []
            }
            
            for itinerary in offer.get("itineraries", []):
                segments = []
                for segment in itinerary.get("segments", []):
                    segments.append({
                        "departure": {
                            "airport": segment.get("departure", {}).get("iataCode"),
                            "terminal": segment.get("departure", {}).get("terminal"),
                            "time": segment.get("departure", {}).get("at")
                        },
                        "arrival": {
                            "airport": segment.get("arrival", {}).get("iataCode"),
                            "terminal": segment.get("arrival", {}).get("terminal"),
                            "time": segment.get("arrival", {}).get("at")
                        },
                        "airline": {
                            "code": segment.get("carrierCode"),
                            "name": self.get_airline_name(segment.get("carrierCode"))
                        },
                        "flight_number": segment.get("number"),
                        "duration": segment.get("duration"),
                        "aircraft": {
                            "code": segment.get("aircraft", {}).get("code"),
                            "name": self._get_aircraft_name(segment.get("aircraft", {}).get("code"))
                        },
                        "operating": {
                            "code": segment.get("operating", {}).get("carrierCode"),
                            "name": self.get_airline_name(segment.get("operating", {}).get("carrierCode"))
                        }
                    })
                flight["itineraries"].append({
                    "duration": itinerary.get("duration"),
                    "segments": segments
                })
            
            processed_flights.append(flight)
        
        return {
            "status": "success",
            "flights": processed_flights,
            "meta": response_data.get("meta", {}),
            "dictionaries": response_data.get("dictionaries", {})
        }

    def get_airline_name(self, airline_code: str) -> str:
        """
        Get airline name from code, using cache if available.
        
        Args:
            airline_code (str): Airline IATA code
            
        Returns:
            str: Airline name or "Unknown Airline" if not found
        """
        if not airline_code:
            return "Unknown Airline"
            
        if airline_code in self.airlines:
            return self.airlines[airline_code]

        try:
            response = requests.get(
                f"{self.base_url}/v1/reference-data/airlines?airlineCodes={airline_code}",
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                airline_data = response.json()
                if airline_data.get("data"):
                    airline_name = airline_data["data"][0]["businessName"]
                    self.airlines[airline_code] = airline_name
                    return airline_name
                    
            return "Unknown Airline"
            
        except Exception:
            return "Unknown Airline"

    def _get_aircraft_name(self, aircraft_code: str) -> str:
        """
        Get aircraft name from code.
        
        Args:
            aircraft_code (str): Aircraft code
            
        Returns:
            str: Aircraft name or "Unknown Aircraft" if not found
        """
        if not aircraft_code:
            return "Unknown Aircraft"
            
        try:
            response = requests.get(
                f"{self.base_url}/v1/reference-data/aircraft?aircraftCodes={aircraft_code}",
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                aircraft_data = response.json()
                if aircraft_data.get("data"):
                    return aircraft_data["data"][0]["name"]
                    
            return "Unknown Aircraft"
            
        except Exception:
            return "Unknown Aircraft"