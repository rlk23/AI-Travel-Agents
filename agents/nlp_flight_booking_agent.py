from typing import Dict
from .city_to_airport_agent import CityToAirportAgent
from .flight_search_agent import FlightSearchAgent
# Import your language model if you're using one
# from langchain_openai import ChatOpenAI

class NLPFlightBookingAgent:
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize NLP Flight Booking Agent with API credentials
        
        Args:
            api_key (str): Amadeus API key
            api_secret (str): Amadeus API secret
        """
        # Initialize city to airport agent
        self.city_agent = CityToAirportAgent(api_key, api_secret)
        
        # Initialize flight search agent with the same access token
        self.flight_agent = FlightSearchAgent(self.city_agent.access_token)
        
        # Initialize language model if you're using one
        # self.llm = ChatOpenAI(...)
        
    def parse_prompt(self, prompt: str) -> Dict:
        """
        Parse user prompt to extract booking details
        
        Args:
            prompt (str): User's natural language prompt
            
        Returns:
            Dict: Extracted booking details
        """
        # This is a simplified example. In practice, you would use LLM or NLP techniques
        booking_details = {
            "Origin city": None,
            "Destination city": None,
            "Departure date": None,
            "Return date": None,
            "Trip type": "one-way",
            "Passengers": 1,
            "Cabin class": "ECONOMY",
            "Hotel stay required": "No",
            "Hotel check-in date": None,
            "Hotel check-out date": None
        }
        
        # Simple parsing for demonstration purposes
        if "from" in prompt.lower():
            parts = prompt.lower().split("from ")
            if len(parts) > 1:
                city_part = parts[1].split(" to ")
                if len(city_part) > 1:
                    booking_details["Origin city"] = city_part[0].strip().title()
                    dest_part = city_part[1].split(" on ")
                    booking_details["Destination city"] = dest_part[0].strip().title()
        
        # Extract date
        if "on" in prompt.lower():
            date_part = prompt.lower().split("on ")
            if len(date_part) > 1:
                booking_details["Departure date"] = date_part[1].strip().split(" ")[0]
                
        # Determine if round trip
        if "round trip" in prompt.lower() or "return" in prompt.lower():
            booking_details["Trip type"] = "round-trip"
            # Extract return date logic would go here
            
        # Determine if hotel is required
        if "hotel" in prompt.lower() or "stay" in prompt.lower() or "accommodation" in prompt.lower():
            booking_details["Hotel stay required"] = "Yes"
            # Extract hotel dates logic would go here
            
        # Advanced parsing would use NLP/LLM techniques
        # If you're using a language model, you could do something like:
        # 
        # prompt_template = """
        # Extract the following travel booking details from the user query:
        # - Origin city
        # - Destination city
        # - Departure date (YYYY-MM-DD format)
        # - Return date (YYYY-MM-DD format, if round-trip)
        # - Trip type (one-way or round-trip)
        # - Number of passengers
        # - Cabin class (ECONOMY, BUSINESS, FIRST)
        # - Whether hotel is required (Yes/No)
        # - Hotel check-in date (if hotel required)
        # - Hotel check-out date (if hotel required)
        # 
        # User query: {user_prompt}
        # 
        # Respond with a JSON object containing only the extracted fields.
        # """
        # result = self.llm.invoke(prompt_template.format(user_prompt=prompt))
        # try:
        #     parsed_result = json.loads(result)
        #     # Validate and merge with default values
        #     for key in booking_details:
        #         if key in parsed_result and parsed_result[key]:
        #             booking_details[key] = parsed_result[key]
        # except:
        #     pass
            
        return booking_details
        
    def process_booking_request(self, prompt: str) -> Dict:
        """
        Process a complete booking request from natural language prompt
        
        Args:
            prompt (str): User's natural language prompt
            
        Returns:
            Dict: Complete booking information with flight options
        """
        # Parse the booking details from the prompt
        booking_details = self.parse_prompt(prompt)
        
        # Validate necessary information
        if not booking_details["Origin city"] or not booking_details["Destination city"]:
            return {
                "status": "error",
                "error": "Origin and destination cities are required.",
                "booking_details": booking_details
            }
            
        if not booking_details["Departure date"]:
            return {
                "status": "error",
                "error": "Departure date is required.",
                "booking_details": booking_details
            }
            
        # Convert cities to airport codes
        origin_code = self.city_agent.city_to_airport_code(booking_details["Origin city"])
        destination_code = self.city_agent.city_to_airport_code(booking_details["Destination city"])
        
        if not origin_code:
            return {
                "status": "error",
                "error": f"Could not find airport code for {booking_details['Origin city']}.",
                "booking_details": booking_details
            }
            
        if not destination_code:
            return {
                "status": "error",
                "error": f"Could not find airport code for {booking_details['Destination city']}.",
                "booking_details": booking_details
            }
            
        # Search for departure flights
        departure_flights = self.flight_agent.search_flights(
            origin=origin_code,
            destination=destination_code,
            date=booking_details["Departure date"],
            cabin=booking_details["Cabin class"],
            passengers=booking_details["Passengers"]
        )
        
        # Search for return flights if round-trip
        return_flights = None
        if booking_details["Trip type"].lower() == "round-trip" and booking_details["Return date"]:
            return_flights = self.flight_agent.search_flights(
                origin=destination_code,
                destination=origin_code,
                date=booking_details["Return date"],
                cabin=booking_details["Cabin class"],
                passengers=booking_details["Passengers"]
            )
            
        # Handle hotel search if required
        hotels = None
        if booking_details["Hotel stay required"].lower() == "yes":
            # If you have a hotel search agent, you'd use it here
            # hotels = self.hotel_agent.search_hotels(...)
            pass
            
        return {
            "status": "success",
            "booking_details": booking_details,
            "departure_flights": departure_flights,
            "return_flights": return_flights,
            "hotels": hotels
        }