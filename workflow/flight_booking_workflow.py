# flight_booking_workflow.py
from agents.user_interaction_agent import UserInteractionAgent  # Make sure this line is present
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

        # Step 3: Search flights
        flight_data = self.flight_search_agent.search_flights(
            origin_code, destination_code, user_details["date"]
        )

        # Step 4: Format and display results, with price filtering
        self.result_agent.format_results(flight_data, user_details["min_price"], user_details["max_price"])
