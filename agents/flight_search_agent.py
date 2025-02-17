import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from datetime import datetime
import requests
import json

class FlightSearchAgent:
    def __init__(self, access_token):
        self.access_token = access_token
        self.airlines = {}  # Store airline data to minimize API calls

    def search_flights(self, origin, destination, date, cabin="ECONOMY", time="00:00:00", max_offers=5):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "currencyCode": "USD",
            "originDestinations": [
                {
                    "id": "1",
                    "originLocationCode": origin,
                    "destinationLocationCode": destination,
                    "departureDateTimeRange": {
                        "date": date,
                        "time": time
                    }
                }
            ],
            "travelers": [
                {
                    "id": "1",
                    "travelerType": "ADULT"
                }
            ],
            "sources": ["GDS"],
            "searchCriteria": {
                "maxFlightOffers": max_offers,
                "flightFilters": {
                    "cabinRestrictions": [
                        {
                            "cabin": cabin.upper(),
                            "coverage": "MOST_SEGMENTS",
                            "originDestinationIds": ["1"]
                        }
                    ]
                }
            }
        }

        response = requests.post(
            "https://test.api.amadeus.com/v2/shopping/flight-offers",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            flights = response.json()
            return flights
        else:
            print("Error fetching flights:", response.json().get("errors", response.text))
            return {"error": "Failed to retrieve flights"}

    def get_airline_name(self, airline_code):
        """
        Fetch airline name from the Amadeus API based on the airline code.
        """
        if airline_code in self.airlines:
            return self.airlines[airline_code]  # Return cached airline name

        url = f"https://test.api.amadeus.com/v1/reference-data/airlines?airlineCodes={airline_code}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            airline_data = response.json()
            if airline_data["data"]:
                airline_name = airline_data["data"][0]["businessName"]
                self.airlines[airline_code] = airline_name  # Cache result
                return airline_name
        return "Unknown Airline"
