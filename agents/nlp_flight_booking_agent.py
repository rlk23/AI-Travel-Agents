import spacy
import re
from datetime import datetime
from .city_to_airport_agent import CityToAirportAgent
from .flight_search_agent import FlightSearchAgent
from .hotel_search_agent import HotelSearchAgent


class NLPFlightBookingAgent:
    def __init__(self):
        self.city_agent = CityToAirportAgent()
        self.flight_agent = FlightSearchAgent(self.city_agent.access_token)
        self.hotel_agent = HotelSearchAgent(self.city_agent.access_token)
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
            "hotel_check_in": None,
            "hotel_check_out": None,
            "hotel_preferences": None
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
            if len(dates) > 2:
                entities["hotel_check_in"] = dates[2]
                if len(dates) > 3:
                    entities["hotel_check_out"] = dates[3]

        # Extract hotel preferences
        if "hotel" in prompt:
            preferences = re.search(r"hotel.*?(near|budget|type):\s*(.*)", prompt)
            if preferences:
                entities["hotel_preferences"] = preferences.group(2)

        # Extract prices
        price_context = re.search(r"(price|between|range).*?(\d+).*?[-toand]+\s*(\d+)", prompt)
        if price_context:
            entities["price_min"] = float(price_context.group(2))
            entities["price_max"] = float(price_context.group(3))

        print("Parsed Booking Details:", entities)
        return entities

    def book_flight_and_hotel(self, prompt):
        booking_details = self.parse_prompt(prompt)
        origin_code = self.city_agent.city_to_airport_code(booking_details["origin"])
        destination_code = self.city_agent.city_to_airport_code(booking_details["destination"])

        if not origin_code or not destination_code:
            print("Unable to retrieve airport codes. Please check the city names and try again.")
            return

        # Flight Booking
        print("\nBooking Flights...")
        departure_flights = self.flight_agent.search_flights(
            origin_code,
            destination_code,
            booking_details["depart_date"]
        )
        print("\nDeparture Flight Options:")
        self.format_results(departure_flights, booking_details["price_min"], booking_details["price_max"])

        if booking_details["trip_type"] == "round-trip" and booking_details["return_date"]:
            return_flights = self.flight_agent.search_flights(
                destination_code,
                origin_code,
                booking_details["return_date"]
            )
            print("\nReturn Flight Options:")
            self.format_results(return_flights, booking_details["price_min"], booking_details["price_max"])

        # Hotel Booking
        if booking_details.get("hotel_check_in") and booking_details.get("hotel_check_out"):
            print("\nBooking Hotels...")
            hotel_data = self.hotel_agent.search_hotels(
                destination_code,
                booking_details["hotel_check_in"],
                booking_details["hotel_check_out"]
            )
            print("\nHotel Options:")
            self.format_hotel_results(hotel_data)

    def format_results(self, flight_data, min_price=None, max_price=None, max_results=5):
        if "data" not in flight_data:
            print("No flight data available.")
            return

        filtered_flights = [
            flight for flight in flight_data["data"]
            if (min_price is None or float(flight["price"]["total"]) >= min_price) and
               (max_price is None or float(flight["price"]["total"]) <= max_price)
        ]

        if filtered_flights:
            print("\nFiltered Flight Options:")
            for flight in filtered_flights[:max_results]:
                self.display_flight(flight)
        else:
            print("\nNo flights found within the specified price range.")
            print("Displaying the top available flights:")
            for flight in flight_data["data"][:max_results]:
                self.display_flight(flight)

    def display_flight(self, flight):
        print(f"Flight ID: {flight['id']}")
        print(f"Price: {flight['price']['currency']} {flight['price']['total']}")
        for itinerary in flight["itineraries"]:
            print(f"  Duration: {itinerary['duration']}")
            for segment in itinerary["segments"]:
                print(f"    {segment['carrierCode']} {segment['number']}: "
                      f"{segment['departure']['iataCode']} -> {segment['arrival']['iataCode']}")
                print(f"    Departure: {segment['departure']['at']}, Arrival: {segment['arrival']['at']}")
        print("-" * 50)

    def format_hotel_results(self, hotel_data, max_results=5):
        if "data" not in hotel_data:
            print("No hotel data available.")
            return

        print("\nAvailable Hotels:")
        for hotel in hotel_data["data"][:max_results]:
            print(f"Hotel Name: {hotel['hotel']['name']}")
            print(f"Price: {hotel['offers'][0]['price']['currency']} {hotel['offers'][0]['price']['total']}")
            print(f"Check-in: {hotel['offers'][0]['checkInDate']}, Check-out: {hotel['offers'][0]['checkOutDate']}")
            print("-" * 50)
