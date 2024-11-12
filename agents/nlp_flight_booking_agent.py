import spacy 
from datetime import datetime
from city_to_airport_agent import CityToAirportAgent
from flight_search_agent import FlightSearchAgent
from result_compilation_agent import ResultCompilationAgent

class NLPFlightBookingAgent:
    def __init__(self):
        self.city_agent = CityToAirportAgent()
        self.flight_agent = FlightSearchAgent(self.city_agent.access_token)
        self.result_agent = ResultCompilationAgent()
        self.nlp = spacy.load("en_core_web_sm")

    
    def parse_prompt(self,prompt):

        doc = self.nlp(prompt)
        
        # Extract entities and terms
        entities = {"origin": None, "destination": None, "depart_date": None, "return_date": None, "trip_type": None, "price_min": None, "price_max": None}
        
        for ent in doc.ents:
            if ent.label_ == "GPE":  # GPE: Geo-political entity, used for cities
                if not entities["origin"]:
                    entities["origin"] = ent.text
                elif not entities["destination"]:
                    entities["destination"] = ent.text
            elif ent.label_ == "DATE":
                if not entities["depart_date"]:
                    entities["depart_date"] = self.parse_date(ent.text)
                elif not entities["return_date"]:
                    entities["return_date"] = self.parse_date(ent.text)
            elif ent.label_ == "MONEY":
                price = int(ent.text.replace("$", ""))
                if not entities["price_min"]:
                    entities["price_min"] = price
                else:
                    entities["price_max"] = price

        # Determine trip type based on terms in the prompt
        if "round-trip" in prompt or "return" in prompt:
            entities["trip_type"] = "round-trip"
        else:
            entities["trip_type"] = "one-way"
        
        return entities
    


    def parse_date(self, date_text):
        """Convert text date to YYYY-MM-DD format if possible."""
        try:
            return datetime.strptime(date_text, "%B %d").strftime("%Y-%m-%d")
        except ValueError:
            return None  # 


    def book_flight(self, prompt):
        # Step 1: Parse user input to get booking details
        booking_details = self.parse_prompt(prompt)
        origin_code = self.city_agent.city_to_airport_code(booking_details["origin"])
        destination_code = self.city_agent.city_to_airport_code(booking_details["destination"])

        if not origin_code or not destination_code:
            print("Unable to retrieve airport codes. Please check the city names and try again.")
            return

        # Step 2: Search for flights
        departure_flights = self.flight_agent.search_flights(origin_code, destination_code, booking_details["depart_date"])
        
        # Step 3: Display results with filtering
        print("Departure Flight Options:")
        self.result_agent.format_results(departure_flights, booking_details["price_min"], booking_details["price_max"])
        
        if booking_details["trip_type"] == "round-trip" and booking_details["return_date"]:
            return_flights = self.flight_agent.search_flights(destination_code, origin_code, booking_details["return_date"])
            print("\nReturn Flight Options:")
            self.result_agent.format_results(return_flights, booking_details["price_min"], booking_details["price_max"])

if __name__ == "__main__":
    agent = NLPFlightBookingAgent()
    user_prompt = input("Please describe your flight booking: ")
    agent.book_flight(user_prompt)