"""
Unit tests for tools.
"""

import pytest
from app.tools.implementations import (
    WeatherTool,
    GitHubUserLookupTool,
    SummarizeTextTool,
    SystemStatusTool,
    GetWeatherInput,
    GitHubUserLookupInput,
    SummarizeTextInput,
)


@pytest.mark.asyncio
async def test_weather_tool():
    """Test weather tool."""
    tool = WeatherTool()
    input_data = GetWeatherInput(city="London", unit="metric")
    result = await tool.execute(input_data)

    assert result.success is True
    assert result.data is not None
    assert result.data.city == "London"


@pytest.mark.asyncio
async def test_weather_tool_invalid_unit():
    """Test weather tool with invalid unit."""
    with pytest.raises(ValueError):
        GetWeatherInput(city="London", unit="invalid")


@pytest.mark.asyncio
async def test_github_lookup_tool():
    """Test GitHub lookup tool."""
    tool = GitHubUserLookupTool()
    input_data = GitHubUserLookupInput(username="torvalds", include_repos=False)
    result = await tool.execute(input_data)

    # May fail if API key not set, but should handle gracefully
    assert result.success or result.error is not None


@pytest.mark.asyncio
async def test_summarize_text_tool():
    """Test text summarization tool."""
    tool = SummarizeTextTool()
    input_data = SummarizeTextInput(
        text="Python is a high-level programming language. It is easy to learn and has a large community.",
        max_length=50,
    )
    result = await tool.execute(input_data)

    assert result.success is True
    assert result.summary is not None
    assert result.original_length > 0


@pytest.mark.asyncio
async def test_system_status_tool():
    """Test system status tool."""
    tool = SystemStatusTool()
    result = await tool.execute()

    assert result.success is True
    assert result.data is not None
    assert result.data.cpu_percent >= 0
    assert result.data.memory_percent >= 0
    assert result.data.uptime_seconds > 0
