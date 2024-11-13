from agents.nlp_flight_booking_agent import NLPFlightBookingAgent

if __name__ == "__main__":
    agent = NLPFlightBookingAgent()
    user_prompt = input("Please describe your flight booking: ")
    agent.book_flight(user_prompt)
