""""
Tests for DataCleaner.
"""

import pandas as pd
import pytest
from src.datacleaning import DataCleaner

@pytest.fixture
def sample_raw_data() -> dict:
    return {
        "coord": {"lon": -0.1257, "lat": 51.5085},
        "weather": [
            {"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04n"}
        ],
        "base": "stations",
        "main": {
            "temp": 22.33,
            "feels_like": 22.34,
            "temp_min": 20.01,
            "temp_max": 23.3,
            "pressure": 1022,
            "humidity": 66,
        },
        "visibility": 10000,
        "wind": {"speed": 1.79, "deg": 68, "gust": 5.81},
        "clouds": {"all": 54},
        "dt": 1784066056,
        "sys": {"type": 2, "id": 2075535, "country": "GB", "sunrise": 1784001563, "sunset": 1784059972},
        "timezone": 3600,
        "id": 2643743,
        "name": "London",
        "cod": 200,
    }
def test_clean_returns_dataframe(sample_raw_data):
    cleaner = DataCleaner()
    result = cleaner.clean(sample_raw_data)
    assert isinstance(result, pd.DataFrame)

def test_clean_returns_one_row(sample_raw_data):
    cleaner = DataCleaner()
    result = cleaner.clean(sample_raw_data)
    assert len(result) == 1

def test_clean_extracts_correct_values(sample_raw_data):
    cleaner = DataCleaner()
    result = cleaner.clean(sample_raw_data)
    row = result.iloc[0]

    assert row["city"] == "London"
    assert row["country"] == "GB"
    assert row["temperature"] == 22.33
    assert row["humidity"] == 66
    assert row["condition"] == "Clouds"
    assert row["description"] == "broken clouds"

def test_clean_converts_timestamp(sample_raw_data):
    """clean() should convert the Unix dt field to a real datetime."""
    cleaner = DataCleaner()
    result = cleaner.clean(sample_raw_data)
    assert pd.api.types.is_datetime64_any_dtype(result["timestamp"])


def test_clean_missing_field_raises_keyerror(sample_raw_data):
    """clean() should raise KeyError if an expected field is missing."""
    broken_data = sample_raw_data.copy()
    del broken_data["main"]  # remove a required field

    cleaner = DataCleaner()
    with pytest.raises(KeyError):
        cleaner.clean(broken_data)   