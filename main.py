import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.nlp_flight_booking_agent import NLPFlightBookingAgent

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize NLP agent
nlp_agent = NLPFlightBookingAgent()

@app.route("/api/ai-agent", methods=["POST"])
def ai_agent():
    data = request.json
    user_prompt = data.get("prompt", "")

    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # Parse the user prompt
        booking_details = nlp_agent.parse_prompt(user_prompt)
        print("Parsed Booking Details:", booking_details)  # Debugging output

        # Validate cities
        origin = booking_details.get("Origin city")
        destination = booking_details.get("Destination city")
        if not origin or not destination:
            return jsonify({"error": "Origin or Destination city is missing"}), 400

        # Fetch airport codes
        origin_code = nlp_agent.city_agent.city_to_airport_code(origin)
        destination_code = nlp_agent.city_agent.city_to_airport_code(destination)
        if not origin_code or not destination_code:
            return jsonify({"error": f"Could not fetch airport codes for {origin} or {destination}"}), 400

        # Validate dates
        depart_date = booking_details.get("Departure date")
        return_date = booking_details.get("Return date")
        if not depart_date:
            return jsonify({"error": "Departure date is required"}), 400
        if booking_details.get("Trip type") == "round-trip" and not return_date:
            return jsonify({"error": "Return date is required for round-trip"}), 400

        # Fetch flights
        departure_flights = fetch_flights(origin_code, destination_code, depart_date, max_results=5)
        return_flights = None
        if return_date:
            return_flights = fetch_flights(destination_code, origin_code, return_date, max_results=5)

        # Handle hotel booking if requested
        hotels = None
        if booking_details.get("Hotel stay required", "").lower() == "yes":
            hotel_check_in = booking_details.get("Hotel check-in date")
            hotel_check_out = booking_details.get("Hotel check-out date")
            if not hotel_check_in or not hotel_check_out:
                return jsonify({
                    "error": "Hotel check-in and check-out dates are required",
                    "booking_details": booking_details
                }), 400
            hotels = fetch_hotels_with_retry(destination_code, hotel_check_in, hotel_check_out, max_results=5)

        # Compile and return the response
        return jsonify({
            "departure_flights": departure_flights,
            "return_flights": return_flights,
            "hotels": hotels,
            "booking_details": booking_details
        }), 200

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


def fetch_flights(origin, destination, date, max_results=5):
    """
    Fetch flights from the API using the FlightSearchAgent and format the results.
    """
    if not date:
        return {"error": "Flight date is required"}

    flights = nlp_agent.flight_agent.search_flights(origin, destination, date)
    if "error" in flights:
        return {"error": flights["error"]}

    # Parse and structure the flight data
    formatted_flights = []
    for flight in flights["data"][:max_results]:
        carrier_code = flight["itineraries"][0]["segments"][0]["carrierCode"]
        airline_name = nlp_agent.flight_agent.get_airline_name(carrier_code)

        flight_info = {
            "flight_id": flight["id"],
            "airline": airline_name,  # Add airline name
            "price": flight["price"]["total"],
            "currency": flight["price"]["currency"],
            "duration": flight["itineraries"][0]["duration"],
            "segments": []
        }

        for segment in flight["itineraries"][0]["segments"]:
            segment_info = {
                "departure_airport": segment["departure"]["iataCode"],
                "departure_time": segment["departure"]["at"],
                "arrival_airport": segment["arrival"]["iataCode"],
                "arrival_time": segment["arrival"]["at"],
                "carrier_code": segment["carrierCode"],
                "airline_name": airline_name,  # Add airline name for each segment
                "flight_number": segment["number"],
                "duration": segment["duration"]
            }
            flight_info["segments"].append(segment_info)

        formatted_flights.append(flight_info)

    return formatted_flights


def fetch_hotels_with_retry(destination_code, check_in, check_out, max_results=5, retries=3, delay=2):
    """
    Fetch hotel data with retry logic to handle rate limits.
    """
    if not check_in or not check_out:
        return {"error": "Hotel check-in and check-out dates are required."}

    for attempt in range(retries):
        try:
            hotels = nlp_agent.hotel_agent.search_hotels(destination_code, check_in, check_out)
            if "data" in hotels and hotels["data"]:
                return [
                    {
                        "hotel_name": hotel["hotel"]["name"],
                        "price": hotel["offers"][0]["price"]["total"],
                        "currency": hotel["offers"][0]["price"]["currency"],
                        "check_in": hotel["offers"][0]["checkInDate"],
                        "check_out": hotel["offers"][0]["checkOutDate"]
                    } for hotel in hotels["data"][:max_results]
                ]
        except Exception as e:
            app.logger.warning(f"Retry {attempt + 1}/{retries} failed: {e}")
            time.sleep(delay)
    return {"error": "Unable to fetch hotel data due to rate limits."}


if __name__ == "__main__":
    app.run(debug=True, port=5002)