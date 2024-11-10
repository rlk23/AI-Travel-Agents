# agents/user_interaction_agent.py
from datetime import datetime

class UserInteractionAgent:
    def collect_details(self):
        # Collecting required details from the user
        origin_city = input("Enter departure city: ")
        destination_city = input("Enter destination city: ")
        date = self.validate_date(input("Enter travel date (YYYY-MM-DD): "))
        
        # Collecting optional price range
        min_price = self.validate_price(input("Enter minimum price (optional): "))
        max_price = self.validate_price(input("Enter maximum price (optional): "))

        return {
            "origin_city": origin_city,
            "destination_city": destination_city,
            "date": date,
            "min_price": min_price,
            "max_price": max_price
        }

    def validate_date(self, date_str):
        """Validates and formats the date input."""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return None

    def validate_price(self, price_str):
        """Validates if price is numeric, returns None if empty or invalid."""
        return float(price_str) if price_str.isnumeric() else None
