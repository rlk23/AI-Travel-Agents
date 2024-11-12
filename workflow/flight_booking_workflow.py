from agents.user_interaction_agent import UserInteractionAgent
from agents.city_to_airport_agent import CityToAirportAgent
from agents.flight_search_agent import FlightSearchAgent
from agents.result_compilation_agent import ResultCompilationAgent

class FlightBookingWorkflow:
    def __init__(self):
        # Initialize the agents
        self.user_agent = UserInteractionAgent()
        self.city_to_airport_agent = CityToAirportAgent()
        self.flight_search_agent = FlightSearchAgent(self.city_to_airport_agent.access_token)
        self.result_agent = ResultCompilationAgent()

    def run(self):
        # Step 1: Collect user details
        user_details = self.user_agent.collect_details()
        
        # Step 2: Convert city names to airport codes
        origin_code = self.city_to_airport_agent.city_to_airport_code(user_details["origin_city"])
        destination_code = self.city_to_airport_agent.city_to_airport_code(user_details["destination_city"])
        
        if not origin_code or not destination_code:
            print("Unable to retrieve airport codes. Please check the city names and try again.")
            return

        # Step 3: Search for departure flights
        print("Searching for departure flights...")
        departure_flight_data = self.flight_search_agent.search_flights(
            origin_code, destination_code, user_details["date"]
        )
        print("Departure Flight Options:")
        self.result_agent.format_results(departure_flight_data, user_details["min_price"], user_details["max_price"])

        # Step 4: Handle round-trip case
        if user_details.get("return_date"):
            print("Searching for return flights...")
            # Ensure the origin and destination are reversed for the return trip
            return_flight_data = self.flight_search_agent.search_flights(
                destination_code, origin_code, user_details["return_date"]
            )
            print("Return Flight Options:")
            self.result_agent.format_results(return_flight_data, user_details["min_price"], user_details["max_price"])
