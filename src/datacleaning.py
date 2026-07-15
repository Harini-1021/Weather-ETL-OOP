"""
Transforms raw OpenWeatherMap JSON into a clean pandas DataFrame.
"""

from datetime import datetime
from typing import Any

import pandas as pd

from src.logger_config import get_logger
logger = get_logger(__name__)

class DataCleaner:

    def clean(self, raw_data: dict[str, Any]) -> pd.DataFrame:
        """
        Convert a single raw OpenWeatherMap response into a one-row DataFrame.

        Args:
            raw_data: The raw JSON dict returned by DataFetcher.

        Returns:
            A pandas DataFrame with one row of cleaned weather data.

        Raises:
            KeyError: if an expected field is missing from raw_data.
        """
        logger.debug(f"CLeaning raw data for city: {raw_data.get('name','unknown')}")

        try:
            record = {
                "city": raw_data["name"],
                "country": raw_data["sys"]["country"],
                "temperature": raw_data["main"]["temp"],
                "feels_like": raw_data["main"]["feels_like"],
                "humidity": raw_data["main"]["humidity"],
                "pressure": raw_data["main"]["pressure"],
                "condition": raw_data["weather"][0]["main"],
                "description": raw_data["weather"][0]["description"],
                "wind_speed": raw_data["wind"]["speed"],
                "cloudiness_pct": raw_data["clouds"]["all"],
                "timestamp": self._convert_timestamp(raw_data["dt"]),
            }
        except (KeyError, IndexError) as e:
            logger.error(f"Missing expected field in raw data: {e}")
            raise 

        df = pd.DataFrame([record])
        logger.info(f"Cleaned data for {record['city']}: 1 row produced")
        return df
    
    def _convert_timestamp(self, unix_ts:int) -> datetime:
        return datetime.fromtimestamp(unix_ts)