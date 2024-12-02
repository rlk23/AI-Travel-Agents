from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
flight_api_key = os.getenv('FLIGHT_API_KEY')
flight_api_secret = os.getenv('FLIGHT_API_SECRET')
hotel_api_key = os.getenv('HOTEL_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
chatgpt_api_key = os.getenv('CHATGPT_API_KEY')
langchain_api_key = os.getenv('LANGCHAIN_API_KEY')


