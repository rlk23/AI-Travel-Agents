from agents.nlp_flight_booking_agent import NLPFlightBookingAgent
from agents.result_compilation_agent import ResultCompilationAgent

if __name__ == "__main__":
    # Initialize the NLP agent and result compilation agent
    nlp_agent = NLPFlightBookingAgent()
    result_agent = ResultCompilationAgent()

    # Get the user input
    user_prompt = input("Please describe your travel plans: ")

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
        print("\nSearching for Departure Flights...")
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
            print("\nSearching for Return Flights...")
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

        # Search hotels if hotel dates are provided
        if booking_details.get("hotel_check_in") and booking_details.get("hotel_check_out"):
            print("\nSearching for Hotels...")
            hotel_data = nlp_agent.hotel_agent.search_hotels(
                city_code=destination_code,
                check_in_date=booking_details["hotel_check_in"],
                check_out_date=booking_details["hotel_check_out"]
            )

            if "data" in hotel_data:
                print("\nHotel Options:")
                result_agent.format_hotel_results(hotel_data, max_results=5)
            else:
                print("\nNo hotel data available.")

        # Optional prompt to finalize booking
        finalize_booking = input("\nWould you like to proceed with the booking? (yes/no): ").strip().lower()
        if finalize_booking == "yes":
            print("Booking confirmation feature is under development. Stay tuned!")
        else:
            print("Thank you for using our travel agent. Have a great day!")
