# result_compilation_agent.py
class ResultCompilationAgent:
    def format_results(self, flight_data, min_price=None, max_price=None):
        if "data" not in flight_data:
            print("No flight data available.")
            if "error" in flight_data:
                print(f"Error: {flight_data['error']}")
            return

        # Filter flights based on min_price and max_price
        filtered_flights = [
            flight for flight in flight_data["data"]
            if (min_price is None or float(flight["price"]["total"]) >= min_price) and
               (max_price is None or float(flight["price"]["total"]) <= max_price)
        ]

        if not filtered_flights:
            print("No flights found within the specified price range.")
            return

        for flight in filtered_flights:
            print(f"Flight ID: {flight['id']}")
            print(f"Price: {flight['price']['currency']} {flight['price']['total']}")
            for itinerary in flight["itineraries"]:
                print(f"  Duration: {itinerary['duration']}")
                for segment in itinerary["segments"]:
                    print(f"    {segment['carrierCode']} {segment['number']}: {segment['departure']['iataCode']} -> {segment['arrival']['iataCode']}")
                    print(f"    Departure: {segment['departure']['at']}, Arrival: {segment['arrival']['at']}")
            print("\n" + "-"*50)
