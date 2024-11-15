import spacy
import re
from datetime import datetime
from .city_to_airport_agent import CityToAirportAgent
from .flight_search_agent import FlightSearchAgent
from .result_compilation_agent import ResultCompilationAgent

class NLPFlightBookingAgent:
    def __init__(self):
        self.city_agent = CityToAirportAgent()
        self.flight_agent = FlightSearchAgent(self.city_agent.access_token)
        self.result_agent = ResultCompilationAgent()
        self.nlp = spacy.load("en_core_web_sm")

    def parse_prompt(self, prompt):
        doc = self.nlp(prompt)

        # Initialize entities
        entities = {
            "origin": None,
            "destination": None,
            "depart_date": None,
            "return_date": None,
            "trip_type": "one-way",
            "price_min": None,
            "price_max": None
        }

        # Extract GPE entities for origin and destination
        gpe_entities = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
        if len(gpe_entities) >= 2:
            entities["origin"] = gpe_entities[0]
            entities["destination"] = gpe_entities[1]
        elif len(gpe_entities) == 1:
            entities["origin"] = gpe_entities[0]

        # Use regex to extract dates in YYYY-MM-DD format
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        dates = re.findall(date_pattern, prompt)
        if dates:
            entities["depart_date"] = dates[0]
            if len(dates) > 1:
                entities["return_date"] = dates[1]
                entities["trip_type"] = "round-trip"

        # If dates are not in YYYY-MM-DD, try to extract them using spaCy
        else:
            date_entities = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
            parsed_dates = [self.parse_date(date_str) for date_str in date_entities]
            parsed_dates = [date for date in parsed_dates if date]
            if parsed_dates:
                entities["depart_date"] = parsed_dates[0]
                if len(parsed_dates) > 1:
                    entities["return_date"] = parsed_dates[1]
                    entities["trip_type"] = "round-trip"

        # Extract price range based on context keywords
        price_context = re.search(r"(price|between|range).*?(\d+).*?[-toand]+\s*(\d+)", prompt)
        if price_context:
            entities["price_min"] = float(price_context.group(2))
            entities["price_max"] = float(price_context.group(3))

        # Determine trip type based on keywords
        if "round-trip" in prompt or "return" in prompt:
            entities["trip_type"] = "round-trip"

        print("Parsed Booking Details:", entities)
        return entities

    def parse_date(self, date_text):
        """Attempt to parse dates in various common formats."""
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d %B %Y", "%B %d %Y", "%B %d", "%d %B"):
            try:
                return datetime.strptime(date_text, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None

    def book_flight(self, prompt, max_flights=5):
        booking_details = self.parse_prompt(prompt)
        origin_code = self.city_agent.city_to_airport_code(booking_details["origin"])
        destination_code = self.city_agent.city_to_airport_code(booking_details["destination"])

        if not origin_code or not destination_code:
            print("Unable to retrieve airport codes. Please check the city names and try again.")
            return

        # Retrieve and display multiple departure flights
        departure_flights = self.flight_agent.search_flights(
            origin_code,
            destination_code,
            booking_details["depart_date"]
        )

        print("Departure Flight Options:")
        self.result_agent.format_results(
            departure_flights,
            booking_details["price_min"],
            booking_details["price_max"],
            max_results=max_flights  # Display up to max_flights
        )

        # Retrieve and display multiple return flights if round-trip
        if booking_details["trip_type"] == "round-trip" and booking_details["return_date"]:
            return_flights = self.flight_agent.search_flights(
                destination_code,
                origin_code,
                booking_details["return_date"]
            )
            print("\nReturn Flight Options:")
            self.result_agent.format_results(
                return_flights,
                booking_details["price_min"],
                booking_details["price_max"],
                max_results=max_flights  # Display up to max_flights
            )
