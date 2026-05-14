"""
Unit tests for schemas.
"""

import pytest
from pydantic import ValidationError
from app.schemas.tools import (
    GetWeatherInput, GitHubUserLookupInput, SummarizeTextInput,
    SystemStatusOutput, WeatherData,
)


def test_get_weather_input_valid():
    """Test valid weather input."""
    input_data = GetWeatherInput(city="London", unit="metric")
    assert input_data.city == "London"
    assert input_data.unit == "metric"


def test_get_weather_input_invalid_unit():
    """Test invalid weather input unit."""
    with pytest.raises(ValidationError):
        GetWeatherInput(city="London", unit="invalid_unit")


def test_get_weather_input_empty_city():
    """Test weather input with empty city."""
    with pytest.raises(ValidationError):
        GetWeatherInput(city="")


def test_github_user_lookup_input_valid():
    """Test valid GitHub lookup input."""
    input_data = GitHubUserLookupInput(username="torvalds", include_repos=True)
    assert input_data.username == "torvalds"
    assert input_data.include_repos is True


def test_github_user_lookup_input_invalid_username():
    """Test GitHub input with invalid username."""
    with pytest.raises(ValidationError):
        # Username with invalid characters
        GitHubUserLookupInput(username="user@invalid")


def test_summarize_text_input_valid():
    """Test valid summarize text input."""
    text = "This is a test text that should be summarized."
    input_data = SummarizeTextInput(text=text, max_length=100)
    assert input_data.text == text
    assert input_data.max_length == 100


def test_summarize_text_input_short_text():
    """Test summarize input with text too short."""
    with pytest.raises(ValidationError):
        SummarizeTextInput(text="short")


def test_weather_data_schema():
    """Test weather data schema."""
    data = WeatherData(
        city="London",
        country="GB",
        temperature=15.0,
        feels_like=14.0,
        humidity=65,
        pressure=1013,
        description="Cloudy",
        wind_speed=5.0,
        cloudiness=50,
    )
    
    assert data.city == "London"
    assert data.temperature == 15.0
    assert data.humidity == 65
