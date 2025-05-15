import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# api_key = os.getenv('API_KEY')  # Get the value of API_KEY
# base_url = os.getenv('BASE_URL')  # Get the value of BASE_URL
# print(api_key, base_url)


class Config:
    """Base configuration."""
    API_KEY = os.getenv('API_KEY') 
    DEBUG = os.getenv("DEBUG", "True") == "True"  # Convert string to bool
    BASE_URL = os.getenv('BASE_URL')  # Get the