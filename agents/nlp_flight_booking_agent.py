from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from datetime import datetime
from .city_to_airport_agent import CityToAirportAgent
from .flight_search_agent import FlightSearchAgent
from .load_environement import chatgpt_api_key
import json


class NLPFlightBookingAgent:
    def __init__(self):
        self.city_agent = CityToAirportAgent()
        self.flight_agent = FlightSearchAgent(self.city_agent.access_token)
        self.llm = ChatOpenAI(model="gpt-4", openai_api_key=chatgpt_api_key)

    def parse_prompt(self, prompt):
        """
        Parse the user input using LangChain and extract required booking details.
        """
        # Update the template to include hotel details
        template = """
        Extract the following information from the input:
        - Origin city
        - Destination city
        - Departure date (yyyy-mm-dd format)
        - Return date (yyyy-mm-dd format, if mentioned)
        - Trip type (one-way or round-trip)
        - Minimum price range (if mentioned)
        - Maximum price range (if mentioned)
        - Hotel stay required (yes or no)
        - Hotel check-in date (yyyy-mm-dd format, if mentioned)
        - Hotel check-out date (yyyy-mm-dd format, if mentioned)

        Input: {prompt}

        Output the result as a JSON object.
        """
        prompt_template = PromptTemplate(input_variables=["prompt"], template=template)
        formatted_prompt = prompt_template.format_prompt(prompt=prompt).to_string()

        try:
            # Send the prompt to the LLM
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
        if "depart_date" in entities and entities["depart_date"]:
            depart_date = datetime.strptime(entities["depart_date"], "%Y-%m-%d")
            if depart_date < today:
                print(f"Invalid depart_date: {entities['depart_date']} (Date is in the past)")
                entities["depart_date"] = None

        if "return_date" in entities and entities["return_date"]:
            return_date = datetime.strptime(entities["return_date"], "%Y-%m-%d")
            if return_date < today:
                print(f"Invalid return_date: {entities['return_date']} (Date is in the past)")
                entities["return_date"] = None
            elif entities["depart_date"]:
                depart_date = datetime.strptime(entities["depart_date"], "%Y-%m-%d")
                if return_date <= depart_date:
                    print(f"Invalid return_date: {entities['return_date']} (Return date must be after depart_date)")
                    entities["return_date"] = None

        if "hotel_check_in" in entities and entities["hotel_check_in"]:
            check_in = datetime.strptime(entities["hotel_check_in"], "%Y-%m-%d")
            if check_in < today:
                print(f"Invalid hotel_check_in: {entities['hotel_check_in']} (Date is in the past)")
                entities["hotel_check_in"] = None

        if "hotel_check_out" in entities and entities["hotel_check_out"]:
            check_out = datetime.strptime(entities["hotel_check_out"], "%Y-%m-%d")
            if check_out <= entities.get("hotel_check_in", today):
                print(f"Invalid hotel_check_out: {entities['hotel_check_out']} (Must be after check-in)")
                entities["hotel_check_out"] = None

        return entities

    def fetch_hotels(self, city_code, check_in, check_out):
        """
        Fetch hotel information for the given city and dates.
        """
        if not check_in or not check_out:
            return {"error": "Check-in and check-out dates are required to fetch hotels"}

        hotels = self.city_agent.fetch_hotels(city_code, check_in, check_out)
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
            } for hotel in hotels.get("data", [])[:5]
        ]

    def book_flight(self, prompt):
        """
        Book flights and optionally fetch hotel details based on extracted booking details.
        """
        booking_details = self.parse_prompt(prompt)
        booking_details = self.validate_dates(booking_details)

        # Get airport codes
        origin_code = self.city_agent.city_to_airport_code(booking_details.get("Origin city"))
        destination_code = self.city_agent.city_to_airport_code(booking_details.get("Destination city"))

        if not origin_code or not destination_code:
            return {"error": "Invalid city names or airport codes could not be retrieved"}

        # Fetch departure flights
        departure_flights = self.flight_agent.search_flights(
            origin_code,
            destination_code,
            booking_details.get("Departure date")
        )

        # Fetch return flights (if applicable)
        return_flights = None
        if booking_details.get("Trip type") == "round-trip" and booking_details.get("Return date"):
            return_flights = self.flight_agent.search_flights(
                destination_code,
                origin_code,
                booking_details.get("Return date")
            )

        # Fetch hotels (if requested)
        hotel_details = None
        if booking_details.get("Hotel stay required", "").lower() == "yes":
            check_in = booking_details.get("hotel_check_in")
            check_out = booking_details.get("hotel_check_out")
            if not check_in or not check_out:
                return {"error": "Hotel check-in and check-out dates are required"}
            hotel_details = self.fetch_hotels(destination_code, check_in, check_out)

        return {
            "departure_flights": departure_flights,
            "return_flights": return_flights,
            "hotel_details": hotel_details,
            "booking_details": booking_details
        }
