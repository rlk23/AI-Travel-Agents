import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.nlp_flight_booking_agent import NLPFlightBookingAgent
from agents.result_compilation_agent import ResultCompilationAgent

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize agents
nlp_agent = NLPFlightBookingAgent()
result_agent = ResultCompilationAgent()

@app.route("/api/ai-agent", methods=["POST"])
def ai_agent():
    data = request.json
    user_prompt = data.get("prompt", "")

    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # Parse user prompt
        booking_details = nlp_agent.parse_prompt(user_prompt)
        origin_code = nlp_agent.city_agent.city_to_airport_code(booking_details["origin"])
        destination_code = nlp_agent.city_agent.city_to_airport_code(booking_details["destination"])

        if not origin_code or not destination_code:
            return jsonify({"error": "Invalid city names provided"}), 400

        # Fetch flights
        departure_data = fetch_flights(origin_code, destination_code, booking_details.get("depart_date"))
        return_data = fetch_flights(destination_code, origin_code, booking_details.get("return_date")) if booking_details.get("trip_type") == "round-trip" else None

        # Fetch hotels
        hotel_data = fetch_hotels_with_retry(
            destination_code,
            booking_details.get("hotel_check_in"),
            booking_details.get("hotel_check_out")
        )

        response = {
            "departure_flights": departure_data,
            "return_flights": return_data,
            "hotels": hotel_data
        }
        return jsonify(response), 200

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

def fetch_flights(origin, destination, date):
    if not date:
        return []
    flights = nlp_agent.flight_agent.search_flights(origin, destination, date)
    return [
        {
            "flight_id": flight["id"],
            "price": flight["price"]["total"],
            "currency": flight["price"]["currency"],
            "departure_code": flight["itineraries"][0]["segments"][0]["departure"]["iataCode"],
            "departure_time": flight["itineraries"][0]["segments"][0]["departure"]["at"],
            "arrival_code": flight["itineraries"][0]["segments"][-1]["arrival"]["iataCode"],
            "arrival_time": flight["itineraries"][0]["segments"][-1]["arrival"]["at"],
            "duration": flight["itineraries"][0]["duration"]
        } for flight in flights["data"][:5]
    ]

def fetch_hotels_with_retry(destination_code, check_in, check_out, retries=3, delay=2):
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
                    } for hotel in hotels["data"][:5]
                ]
        except Exception as e:
            app.logger.warning(f"Retry {attempt + 1}/{retries} failed: {e}")
            time.sleep(delay)
    return {"error": "Unable to fetch hotel data due to rate limits."}

if __name__ == "__main__":
    app.run(debug=True, port=5002)
