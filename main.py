from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.nlp_flight_booking_agent import NLPFlightBookingAgent
from agents.result_compilation_agent import ResultCompilationAgent

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all origins
CORS(app)

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
            return jsonify({"error": "Invalid city names provided"}), 400

        # Fetch departure flights
        departure_flights = nlp_agent.flight_agent.search_flights(
            origin=origin_code,
            destination=destination_code,
            date=booking_details["depart_date"]
        )

        # Organize departure flights
        departure_data = []
        for flight in departure_flights["data"][:5]:
            departure_data.append({
                "flight_id": flight["id"],
                "price": flight["price"]["total"],
                "currency": flight["price"]["currency"],
                "departure_code": flight["itineraries"][0]["segments"][0]["departure"]["iataCode"],
                "departure_time": flight["itineraries"][0]["segments"][0]["departure"]["at"],
                "arrival_code": flight["itineraries"][0]["segments"][-1]["arrival"]["iataCode"],
                "arrival_time": flight["itineraries"][0]["segments"][-1]["arrival"]["at"],
                "duration": flight["itineraries"][0]["duration"]
            })

        # Handle round-trip flights
        return_data = []
        if booking_details["trip_type"] == "round-trip" and booking_details.get("return_date"):
            return_flights = nlp_agent.flight_agent.search_flights(
                origin=destination_code,
                destination=origin_code,
                date=booking_details["return_date"]
            )
            for flight in return_flights["data"][:5]:
                return_data.append({
                    "flight_id": flight["id"],
                    "price": flight["price"]["total"],
                    "currency": flight["price"]["currency"],
                    "departure_code": flight["itineraries"][0]["segments"][0]["departure"]["iataCode"],
                    "departure_time": flight["itineraries"][0]["segments"][0]["departure"]["at"],
                    "arrival_code": flight["itineraries"][0]["segments"][-1]["arrival"]["iataCode"],
                    "arrival_time": flight["itineraries"][0]["segments"][-1]["arrival"]["at"],
                    "duration": flight["itineraries"][0]["duration"]
                })

        # Return the structured response
        response = {
            "departure_flights": departure_data,
            "return_flights": return_data if return_data else None
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    # Run the Flask app in debug mode on port 5002
    app.run(debug=True, port=5002)
