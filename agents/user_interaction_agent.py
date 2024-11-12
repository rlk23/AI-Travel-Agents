from datetime import datetime

class UserInteractionAgent:
    def collect_details(self):
        # Ask if the user wants a one-way or round-trip
        trip_type = input("Is this a one-way trip or a round-trip? (Enter 'one-way' or 'round-trip'): ").strip().lower()
        
        # Collecting required details for departure
        origin_city = input("Enter departure city: ")
        destination_city = input("Enter destination city: ")
        date = self.validate_date(input("Enter travel date (YYYY-MM-DD): "))
        
        # If round-trip, ask for return details
        if trip_type == "round-trip":
            return_date = self.validate_date(input("Enter return date (YYYY-MM-DD): "))
            return_city = destination_city  # Default return to the original destination
            same_return_location = input("Is the return trip to the same location? (yes or no): ").strip().lower()
            if same_return_location == "no":
                return_city = input("Enter the city where you will return to: ")
        else:
            return_date = None
            return_city = None

        # Collecting optional price range
        min_price = self.validate_price(input("Enter minimum price (optional): "))
        max_price = self.validate_price(input("Enter maximum price (optional): "))

        return {
            "origin_city": origin_city,
            "destination_city": destination_city,
            "date": date,
            "trip_type": trip_type,
            "return_date": return_date,
            "return_city": return_city,
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
