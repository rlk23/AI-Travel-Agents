# nlp_flight_booking_agent.py
import spacy
import re
from datetime import datetime
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
            "price_max": None
        }

        # Extract cities
        gpe_entities = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
        if len(gpe_entities) >= 2:
            entities["origin"] = gpe_entities[0]
            entities["destination"] = gpe_entities[1]
        elif len(gpe_entities) == 1:
            entities["origin"] = gpe_entities[0]

        # Extract dates
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        dates = re.findall(date_pattern, prompt)
        if dates:
            entities["depart_date"] = dates[0]
            if len(dates) > 1:
                entities["return_date"] = dates[1]
                entities["trip_type"] = "round-trip"

        # Extract prices
        price_context = re.search(r"(price|between|range).*?(\d+).*?[-toand]+\s*(\d+)", prompt)
        if price_context:
            entities["price_min"] = float(price_context.group(2))
            entities["price_max"] = float(price_context.group(3))

        print("Parsed Booking Details:", entities)
        return entities

    def book_flight(self, prompt):
        booking_details = self.parse_prompt(prompt)
        origin_code = self.city_agent.city_to_airport_code(booking_details["origin"])
        destination_code = self.city_agent.city_to_airport_code(booking_details["destination"])

        if not origin_code or not destination_code:
            print("Unable to retrieve airport codes. Please check the city names and try again.")
            return

        departure_flights = self.flight_agent.search_flights(
            origin_code,
            destination_code,
            booking_details["depart_date"]
        )
        print("Departure Flight Options:", departure_flights)

        if booking_details["trip_type"] == "round-trip" and booking_details["return_date"]:
            return_flights = self.flight_agent.search_flights(
                destination_code,
                origin_code,
                booking_details["return_date"]
            )
            print("Return Flight Options:", return_flights)
