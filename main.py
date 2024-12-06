from flask import Flask, request, Response
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
        return "Error: Prompt is required", 400
    try:
        # Process user prompt
        booking_details = nlp_agent.parse_prompt(user_prompt)

        # Retrieve airport codes
        origin_code = nlp_agent.city_agent.city_to_airport_code(booking_details["origin"])
        destination_code = nlp_agent.city_agent.city_to_airport_code(booking_details["destination"])

        # Validate airport codes
        if not origin_code or not destination_code:
            return "Error: Invalid city names provided.", 400

        # Fetch departure flights
        departure_flights = nlp_agent.flight_agent.search_flights(
            origin=origin_code,
            destination=destination_code,
            date=booking_details["depart_date"]
        )

        response_text = f"Departure Flights:\n"
        for flight in departure_flights["data"][:5]:
            response_text += (
                f"Flight ID: {flight['id']}\n"
                f"  Price: {flight['price']['total']} {flight['price']['currency']}\n"
                f"  Departure: {flight['itineraries'][0]['segments'][0]['departure']['iataCode']} "
                f"({flight['itineraries'][0]['segments'][0]['departure']['at']})\n"
                f"  Arrival: {flight['itineraries'][0]['segments'][-1]['arrival']['iataCode']} "
                f"({flight['itineraries'][0]['segments'][-1]['arrival']['at']})\n"
                f"  Duration: {flight['itineraries'][0]['duration']}\n"
            )

        # Handle round-trip flights
        if booking_details["trip_type"] == "round-trip" and booking_details.get("return_date"):
            return_flights = nlp_agent.flight_agent.search_flights(
                origin=destination_code,
                destination=origin_code,
                date=booking_details["return_date"]
            )
            response_text += "\nReturn Flights:\n"
            for flight in return_flights["data"][:5]:
                response_text += (
                    f"Flight ID: {flight['id']}\n"
                    f"  Price: {flight['price']['total']} {flight['price']['currency']}\n"
                    f"  Departure: {flight['itineraries'][0]['segments'][0]['departure']['iataCode']} "
                    f"({flight['itineraries'][0]['segments'][0]['departure']['at']})\n"
                    f"  Arrival: {flight['itineraries'][0]['segments'][-1]['arrival']['iataCode']} "
                    f"({flight['itineraries'][0]['segments'][-1]['arrival']['at']})\n"
                    f"  Duration: {flight['itineraries'][0]['duration']}\n"
                )

        return Response(response_text, mimetype="text/plain"), 200

    except Exception as e:
        return f"Internal Server Error: {str(e)}", 500

if __name__ == "__main__":
    # Run the Flask app in debug mode on port 5000
    app.run(debug=True, port=5001)
