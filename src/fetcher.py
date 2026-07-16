"""
Data Fetcher : handles all communicatio with the OpenWeatherMap API.
"""

import os
from typing import Any

import requests
from dotenv import load_dotenv
from src.decorators import timer, retry
from src.logger_config import get_logger

load_dotenv()

class DataFetcher:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self,api_key:str | None = None) -> None:
        # Initialize the fetcher with an API key. 
        # If no api_key is passed explicitly, falls back to the 
        # OWN_API_KEY environment variable (loaded from .env)

        self.api_key: str | None = api_key or os.getenv("OWM_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set OWN_API_KEY in .env"
                "or pass api_key explicitly"
            )
        self.session: requests.Session = requests.Session()
    @timer
    @retry(max_attempts=3, delay=1.0)
    def fetch_current_weather(self, city:str, units: str = "metric") -> dict[str,Any]:
        """
        Fetch current weather data for a given city.

        Args:
            city: City name, e.g. "London" or "London,GB".
            units: "metric", "imperial", or "standard".

        Returns:
            Parsed JSON response as a dict.

        Raises:
            ValueError: if city is empty.
            requests.exceptions.RequestException: on network/API errors.
        """
        if not city or not city.strip():
            raise ValueError("City name must not be empty.")
        
        params = {
            "q" : city,
            "appid" : self.api_key,
            "units" : units,
        }

        response = self.session.get(self.BASE_URL, params = params, timeout = 10)
        response.raise_for_status() # raises HTTPError for 4xx/5xx responses

        return response.json()