from agents.nlp_flight_booking_agent import NLPFlightBookingAgent
from agents.result_compilation_agent import ResultCompilationAgent

if __name__ == "__main__":
    # Initialize the NLP agent and result compilation agent
    nlp_agent = NLPFlightBookingAgent()
    result_agent = ResultCompilationAgent()

    # Get the user input
    user_prompt = input("Please describe your flight booking: ")

    # Parse the booking details
    booking_details = nlp_agent.parse_prompt(user_prompt)

    # Retrieve airport codes
    origin_code = nlp_agent.city_agent.city_to_airport_code(booking_details["origin"])
    destination_code = nlp_agent.city_agent.city_to_airport_code(booking_details["destination"])

    # Handle case where airport codes are not found
    if not origin_code or not destination_code:
        print("Unable to retrieve airport codes. Please check the city names and try again.")
    else:
        # Fetch departure flights
        departure_flights = nlp_agent.flight_agent.search_flights(
            origin=origin_code,
            destination=destination_code,
            date=booking_details["depart_date"]
        )

        print("\nDeparture Flight Options:")
        result_agent.format_results(
            flight_data=departure_flights,
            min_price=booking_details["price_min"],
            max_price=booking_details["price_max"],
            max_results=5
        )

        # Fetch return flights if it is a round-trip
        if booking_details["trip_type"] == "round-trip" and booking_details["return_date"]:
            return_flights = nlp_agent.flight_agent.search_flights(
                origin=destination_code,
                destination=origin_code,
                date=booking_details["return_date"]
            )

            print("\nReturn Flight Options:")
            result_agent.format_results(
                flight_data=return_flights,
                min_price=booking_details["price_min"],
                max_price=booking_details["price_max"],
                max_results=5
            )
