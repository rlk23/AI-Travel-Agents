from flask import Flask, request, jsonify
from agents.nlp_flight_booking_agent import NLPFlightBookingAgent
from agents.result_compilation_agent import ResultCompilationAgent

# Initialize Flask app
app = Flask(__name__)

# Initialize agents
nlp_agent = NLPFlightBookingAgent()
result_agent = ResultCompilationAgent()

@app.route("/api/ai-agent", methods=["POST"])
def ai_agent():
    data = request.json
    user_prompt = data.get("prompt", "")

    # Validate the prompt
    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # Process user prompt
        booking_details = nlp_agent.parse_prompt(user_prompt)

        # Retrieve airport codes
        origin_code = nlp_agent.city_agent.city_to_airport_code(booking_details["origin"])
        destination_code = nlp_agent.city_agent.city_to_airport_code(booking_details["destination"])

        # Validate airport codes
        if not origin_code or not destination_code:
            return jsonify({"error": "Invalid city names provided."}), 400

        # Fetch departure flights
        departure_flights = nlp_agent.flight_agent.search_flights(
            origin=origin_code,
            destination=destination_code,
            date=booking_details["depart_date"]
        )

        result_data = {
            "departure_flights": departure_flights,
            "trip_type": booking_details["trip_type"],
        }

        # Fetch return flights for round-trip
        if booking_details["trip_type"] == "round-trip" and booking_details["return_date"]:
            return_flights = nlp_agent.flight_agent.search_flights(
                origin=destination_code,
                destination=origin_code,
                date=booking_details["return_date"]
            )
            result_data["return_flights"] = return_flights

        # Fetch hotel data if applicable
        if booking_details.get("hotel_check_in") and booking_details.get("hotel_check_out"):
            hotel_data = nlp_agent.hotel_agent.search_hotels(
                city_code=destination_code,
                check_in_date=booking_details["hotel_check_in"],
                check_out_date=booking_details["hotel_check_out"]
            )
            result_data["hotels"] = hotel_data

        # Return successful response
        return jsonify(result_data), 200

    except Exception as e:
        # Return error details for debugging
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    # Run the Flask app in debug mode on port 5000
    app.run(debug=True, port=5000)
