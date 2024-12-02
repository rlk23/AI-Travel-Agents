class FlightBookingWorkflow:
    def __init__(self):
        self.user_agent = UserInteractionAgent()
        self.city_to_airport_agent = CityToAirportAgent()
        self.flight_search_agent = FlightSearchAgent(self.city_to_airport_agent.access_token)
        self.hotel_search_agent = HotelSearchAgent(self.city_to_airport_agent.access_token)
        self.result_agent = ResultCompilationAgent()

    def run(self):
        user_details = self.user_agent.collect_details()

        # Step 1: Flight Booking (existing logic)
        origin_code = self.city_to_airport_agent.city_to_airport_code(user_details["origin_city"])
        destination_code = self.city_to_airport_agent.city_to_airport_code(user_details["destination_city"])
        
        departure_flight_data = self.flight_search_agent.search_flights(
            origin_code, destination_code, user_details["date"]
        )
        self.result_agent.format_results(departure_flight_data, user_details["min_price"], user_details["max_price"])

        if user_details.get("return_date"):
            return_flight_data = self.flight_search_agent.search_flights(
                destination_code, origin_code, user_details["return_date"]
            )
            self.result_agent.format_results(return_flight_data, user_details["min_price"], user_details["max_price"])

        # Step 2: Hotel Booking
        hotel_prompt = input("Do you want to book a hotel at your destination? (yes/no): ").strip().lower()
        if hotel_prompt == "yes":
            check_in = input("Enter check-in date (YYYY-MM-DD): ")
            check_out = input("Enter check-out date (YYYY-MM-DD): ")

            hotel_data = self.hotel_search_agent.search_hotels(
                destination_code, check_in, check_out
            )
            print("\nHotel Options:")
            self.result_agent.format_results(hotel_data)
