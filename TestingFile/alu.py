import spacy
import re
from dateutil import parser

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_trip_details(prompt):
    doc = nlp(prompt)
    trip_details = {
        "origin": None,
        "destination": None,
        "departure_date": None,
        "arrival_date": None,
        "min_price": None,
        "max_price": None,
    }
    
    # Extract cities (origin and destination)
    locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    if len(locations) > 1:
        trip_details["origin"] = locations[0]
        trip_details["destination"] = locations[1]
    elif locations:
        trip_details["destination"] = locations[0]
    
    # Extract dates (departure and arrival)
    date_pattern = r"\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{2}[-/]\d{2}|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2}(?:,)?\s\d{4}\b)"
    dates = re.findall(date_pattern, prompt, flags=re.IGNORECASE)
    parsed_dates = []
    for date_str in dates:
        try:
            parsed_date = parser.parse(date_str, fuzzy=True)
            parsed_dates.append(parsed_date.strftime("%Y-%m-%d"))
        except ValueError:
            pass
    
    # Assign dates to departure and arrival
    if len(parsed_dates) >= 1:
        trip_details["departure_date"] = parsed_dates[0]
    if len(parsed_dates) >= 2:
        trip_details["arrival_date"] = parsed_dates[1]
    
    # Extract budget range using regex
    budget_match = re.search(r"\b(\d+)\s*-\s*(\d+)\s*\$", prompt)
    if budget_match:
        trip_details["min_price"] = int(budget_match.group(1))
        trip_details["max_price"] = int(budget_match.group(2))
    
    return trip_details

# Example prompt
prompt = "I want to book a round-trip flight from Atlanta to Houston within the dates of December 12, 2024 and 12-24-2024 with a price range between 200 - 500 $"
details = extract_trip_details(prompt)
print(details)
