import spacy
import re
from datetime import datetime
from dateutil import parser
from .city_to_airport_agent import CityToAirportAgent
from .flight_search_agent import FlightSearchAgent


class NLPFlightBookingAgent:
    def __init__(self):
        self.city_agent = CityToAirportAgent()
        self.flight_agent = FlightSearchAgent(self.city_agent.access_token)
        self.nlp = spacy.load("en_core_web_sm")

    def parse_prompt(self, prompt):
        doc = self.nlp(prompt)
        entities = {
            "origin": None,
            "destination": None,
            "depart_date": None,
            "return_date": None,
            "trip_type": "one-way",
            "price_min": None,
            "price_max": None,
        }

        # Extract cities
        gpe_entities = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
        if len(gpe_entities) >= 2:
            entities["origin"] = gpe_entities[0]
            entities["destination"] = gpe_entities[1]
        elif len(gpe_entities) == 1:
            entities["origin"] = gpe_entities[0]

        # Extract and validate dates
        entities = self.extract_dates(prompt, entities)

        # Extract prices
        price_context = re.search(r"(price|between|range).*?(\d+).*?[-toand]+\s*(\d+)", prompt)
        if price_context:
            entities["price_min"] = float(price_context.group(2))
            entities["price_max"] = float(price_context.group(3))

        # Debugging: Display parsed booking details
        print("Parsed Booking Details:", entities)
        return entities

    def extract_dates(self, prompt, entities):
        """
        Extract and parse multiple date formats using flexible parsing.
        """
        today = datetime.today()
        possible_dates = []

        # Use dateutil.parser to extract flexible dates
        for word in prompt.split():
            try:
                parsed_date = parser.parse(word, fuzzy=True)
                # Filter out past dates and unreasonable years
                if parsed_date >= today and 1900 <= parsed_date.year <= 2100:
                    possible_dates.append(parsed_date)
            except (ValueError, TypeError):
                continue

        # Remove duplicate dates
        unique_dates = list(sorted(set(possible_dates)))

        # Debugging: Display extracted dates
        print("Filtered Dates:", [date.strftime("%Y-%m-%d") for date in unique_dates])

        # Assign dates to entities
        if len(unique_dates) >= 1:
            entities["depart_date"] = unique_dates[0].strftime("%Y-%m-%d")
        if len(unique_dates) >= 2:
            entities["return_date"] = unique_dates[1].strftime("%Y-%m-%d")
            entities["trip_type"] = "round-trip"

        # Validate extracted dates
        entities = self.validate_dates(entities, today)

        return entities

    def validate_dates(self, entities, today):
        """
        Validate the extracted dates to ensure they are logical.
        """
        if entities["depart_date"]:
            depart_date = datetime.strptime(entities["depart_date"], "%Y-%m-%d")
            if depart_date < today:
                print(f"Invalid depart_date: {entities['depart_date']} (Date is in the past)")
                entities["depart_date"] = None

        if entities["return_date"]:
            return_date = datetime.strptime(entities["return_date"], "%Y-%m-%d")
            if return_date < today:
                print(f"Invalid return_date: {entities['return_date']} (Date is in the past)")
                entities["return_date"] = None
            elif entities["depart_date"]:
                depart_date = datetime.strptime(entities["depart_date"], "%Y-%m-%d")
                if return_date <= depart_date:
                    print(f"Invalid return_date: {entities['return_date']} (Return date must be after depart_date)")
                    entities["return_date"] = None

        return entities

    def book_flight(self, prompt):
        """
        Book flights based on extracted booking details.
        """
        booking_details = self.parse_prompt(prompt)

        # Get airport codes
        origin_code = self.city_agent.city_to_airport_code(booking_details["origin"])
        destination_code = self.city_agent.city_to_airport_code(booking_details["destination"])

        if not origin_code or not destination_code:
            print("Invalid city names. Unable to fetch airport codes.")
            return {"error": "Invalid city names"}

        # Book departure flight
        print("\nFetching Departure Flights...")
        departure_flights = self.flight_agent.search_flights(
            origin_code,
            destination_code,
            booking_details["depart_date"]
        )

        # Debugging: Display departure flights
        print("Departure Flights:", departure_flights)

        # Book return flight if applicable
        if booking_details["trip_type"] == "round-trip" and booking_details["return_date"]:
            print("\nFetching Return Flights...")
            return_flights = self.flight_agent.search_flights(
                destination_code,
                origin_code,
                booking_details["return_date"]
            )
            # Debugging: Display return flights
            print("Return Flights:", return_flights)

    def format_results(self, flight_data):
        """
        Format flight data for readability.
        """
        if not flight_data or "data" not in flight_data:
            print("No flight data available.")
            return []

        for flight in flight_data["data"]:
            print(f"Flight ID: {flight['id']} | Price: {flight['price']['total']} {flight['price']['currency']}")
            for itinerary in flight["itineraries"]:
                print(f"Duration: {itinerary['duration']}")
                for segment in itinerary["segments"]:
                    print(f"  {segment['carrierCode']} {segment['number']}: "
                          f"{segment['departure']['iataCode']} -> {segment['arrival']['iataCode']}")
                    print(f"  Departure: {segment['departure']['at']}, Arrival: {segment['arrival']['at']}")
            print("-" * 50)
