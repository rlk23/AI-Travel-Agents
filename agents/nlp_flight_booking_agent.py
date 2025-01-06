from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from datetime import datetime
from .city_to_airport_agent import CityToAirportAgent
from .flight_search_agent import FlightSearchAgent
from .hotel_search_agent import HotelSearchAgent
from .load_environement import chatgpt_api_key
import json

class NLPFlightBookingAgent:
    def __init__(self):
        self.city_agent = CityToAirportAgent()
        self.flight_agent = FlightSearchAgent(self.city_agent.access_token)
        self.hotel_agent = HotelSearchAgent(self.city_agent.access_token)
        self.llm = ChatOpenAI(model="gpt-4", openai_api_key=chatgpt_api_key)

    def parse_prompt(self, prompt):
        """
        Parse the user input using LangChain and extract required booking details.
        """
        template = """
        Extract the following information from the input:
        - Origin city
        - Destination city
        - Departure date (yyyy-mm-dd format)
        - Return date (yyyy-mm-dd format, if mentioned)
        - Trip type (one-way or round-trip)
        - Minimum price range (if mentioned)
        - Maximum price range (if mentioned)
        - Seat class (economy, business, first; default is economy)
        - Hotel stay required (yes or no)
        - Hotel check-in date (yyyy-mm-dd format, if mentioned)
        - Hotel check-out date (yyyy-mm-dd format, if mentioned)

        Input: {prompt}

        Output the result as a JSON object.
        """
        prompt_template = PromptTemplate(input_variables=["prompt"], template=template)
        formatted_prompt = prompt_template.format_prompt(prompt=prompt).to_string()

        try:
            response = self.llm.invoke(formatted_prompt)
            parsed_response = json.loads(response.content)
            print("Parsed Response:", json.dumps(parsed_response, indent=4))
            return parsed_response
        except Exception as e:
            print(f"Error processing LLM response: {e}")
            raise ValueError("Failed to process the prompt.")

    def validate_dates(self, entities):
        """
        Validate and correct extracted dates to ensure they are logical.
        """
        today = datetime.today()

        if "Departure date" in entities:
            depart_date = datetime.strptime(entities["Departure date"], "%Y-%m-%d")
            if depart_date < today:
                print(f"Invalid Departure date: {entities['Departure date']} (Date is in the past)")
                entities["Departure date"] = None

        if "Return date" in entities:
            return_date = datetime.strptime(entities["Return date"], "%Y-%m-%d")
            if return_date < today:
                print(f"Invalid Return date: {entities['Return date']} (Date is in the past)")
                entities["Return date"] = None
            elif entities["Departure date"] and return_date <= datetime.strptime(
                entities["Departure date"], "%Y-%m-%d"
            ):
                print(f"Invalid Return date: {entities['Return date']} (Must be after departure date)")
                entities["Return date"] = None

        if "Hotel check-in date" in entities:
            check_in_date = datetime.strptime(entities["Hotel check-in date"], "%Y-%m-%d")
            if check_in_date < today:
                print(f"Invalid Hotel check-in date: {entities['Hotel check-in date']} (Date is in the past)")
                entities["Hotel check-in date"] = None

        if "Hotel check-out date" in entities:
            check_out_date = datetime.strptime(entities["Hotel check-out date"], "%Y-%m-%d")
            if check_out_date <= entities.get("Hotel check-in date", today):
                print(
                    f"Invalid Hotel check-out date: {entities['Hotel check-out date']} (Must be after check-in date)"
                )
                entities["Hotel check-out date"] = None

        return entities

    def fetch_hotels(self, city_code, check_in, check_out):
        """
        Fetch hotel information for the given city and dates.
        """
        if not check_in or not check_out:
            return {"error": "Check-in and check-out dates are required to fetch hotels"}

        hotels = self.hotel_agent.search_hotels(city_code, check_in, check_out)
        if "error" in hotels:
            return {"error": hotels["error"]}

        # Format hotel data
        return [
            {
                "hotel_name": hotel["hotel"]["name"],
                "price": hotel["offers"][0]["price"]["total"],
                "currency": hotel["offers"][0]["price"]["currency"],
                "check_in": hotel["offers"][0]["checkInDate"],
                "check_out": hotel["offers"][0]["checkOutDate"]
            }
            for hotel in hotels.get("data", [])[:5]
        ]

    def book_flight(self, flight_id, seat_class="economy"):
        """
        Book a flight with the specified flight ID and seat class.
        """
        try:
            booking_response = self.flight_agent.book_flight(
                flight_id=flight_id,
                seat_class=seat_class,
                passenger_details={"name": "John Doe"}  # Example passenger details
            )
            return booking_response
        except Exception as e:
            print(f"Error booking flight: {e}")
            return {"error": "Failed to book the flight"}

    def handle_request(self, prompt):
        """
        Handle the overall request including fetching flights, hotels, and optional booking.
        """
        booking_details = self.parse_prompt(prompt)
        booking_details = self.validate_dates(booking_details)

        origin_code = self.city_agent.city_to_airport_code(booking_details.get("Origin city"))
        destination_code = self.city_agent.city_to_airport_code(booking_details.get("Destination city"))

        if not origin_code or not destination_code:
            return {"error": "Invalid city names or airport codes could not be retrieved"}

        # Fetch flights
        departure_flights = self.flight_agent.search_flights(
            origin_code, destination_code, booking_details.get("Departure date")
        )[:5]

        return_flights = None
        if booking_details.get("Trip type") == "round-trip" and booking_details.get("Return date"):
            return_flights = self.flight_agent.search_flights(
                destination_code, origin_code, booking_details.get("Return date")
            )[:5]

        # Fetch hotels
        hotel_details = None
        if booking_details.get("Hotel stay required", "").lower() == "yes":
            check_in = booking_details.get("Hotel check-in date")
            check_out = booking_details.get("Hotel check-out date")
            hotel_details = self.fetch_hotels(destination_code, check_in, check_out)

        return {
            "departure_flights": departure_flights,
            "return_flights": return_flights,
            "hotel_details": hotel_details,
            "booking_details": booking_details,
        }
