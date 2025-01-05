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
        # Define the template
        template = """
        Extract the following information from the input:
        - Origin city
        - Destination city
        - Departure date (yyyy-mm-dd format)
        - Return date (yyyy-mm-dd format, if mentioned)
        - Trip type (one-way or round-trip)
        - Minimum price range (if mentioned)
        - Maximum price range (if mentioned)

        Input: {prompt}

        Output the result as a JSON object.
        """
        # Format the prompt
        prompt_template = PromptTemplate(input_variables=["prompt"], template=template)
        formatted_prompt = prompt_template.format_prompt(prompt=prompt).to_string()

        try:
            # Send the prompt to the LLM
            response = self.llm.invoke(formatted_prompt)
            # Extract content and parse JSON
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
        return entities

    def book_flight(self, prompt):
        """
        Book flights based on extracted booking details.
        """
        # Extract entities from user prompt
        booking_details = self.parse_prompt(prompt)

        # Validate dates
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

        # Return the result
        return {
            "departure_flights": departure_flights,
            "return_flights": return_flights,
            "booking_details": booking_details
        }
