"""
MCP Tools implementation.
All four tools: get_weather, github_user_lookup, summarize_text, system_status.
"""

import logging
from typing import Dict, Any
from app.schemas.tools import (
    GetWeatherInput,
    GetWeatherOutput,
    WeatherData,
    GitHubUserLookupInput,
    GitHubUserLookupOutput,
    SummarizeTextInput,
    SummarizeTextOutput,
    SystemStatusOutput,
    SystemStatus,
)
from app.services.external_apis import WeatherService, GitHubService, OpenAIService
from app.utils.helpers import get_system_status, measure_execution_time
from app.core.exceptions import ValidationError

logger = logging.getLogger("app")


class WeatherTool:
    """Get weather tool implementation."""

    def __init__(self):
        self.service = WeatherService()

    @measure_execution_time
    async def execute(self, input_data: GetWeatherInput) -> GetWeatherOutput:
        """Execute get_weather tool."""
        try:
            logger.info(f"Fetching weather for {input_data.city}")

            weather_data = await self.service.get_weather(
                city=input_data.city,
                unit=input_data.unit,
            )

            data = WeatherData(**weather_data)

            return GetWeatherOutput(
                success=True,
                data=data,
            )
        except Exception as e:
            logger.error(f"Weather tool error: {str(e)}")
            return GetWeatherOutput(
                success=False,
                error=str(e),
            )


class GitHubUserLookupTool:
    """GitHub user lookup tool implementation."""

    def __init__(self):
        self.service = GitHubService()

    @measure_execution_time
    async def execute(self, input_data: GitHubUserLookupInput) -> GitHubUserLookupOutput:
        """Execute github_user_lookup tool."""
        try:
            logger.info(f"Fetching GitHub user: {input_data.username}")

            user_data = await self.service.get_user(
                username=input_data.username,
                include_repos=input_data.include_repos,
            )

            from app.schemas.tools import GitHubUserData

            data = GitHubUserData(**user_data)

            return GitHubUserLookupOutput(
                success=True,
                data=data,
            )
        except Exception as e:
            logger.error(f"GitHub lookup tool error: {str(e)}")
            return GitHubUserLookupOutput(
                success=False,
                error=str(e),
            )


class SummarizeTextTool:
    """Summarize text tool implementation."""

    def __init__(self):
        self.service = OpenAIService()

    @measure_execution_time
    async def execute(self, input_data: SummarizeTextInput) -> SummarizeTextOutput:
        """Execute summarize_text tool."""
        try:
            logger.info(f"Summarizing text ({len(input_data.text)} characters)")

            summary = await self.service.summarize_text(
                text=input_data.text,
                max_length=input_data.max_length,
            )

            return SummarizeTextOutput(
                success=True,
                summary=summary,
                original_length=len(input_data.text),
                summary_length=len(summary) if summary else 0,
            )
        except Exception as e:
            logger.error(f"Summarize tool error: {str(e)}")
            return SummarizeTextOutput(
                success=False,
                error=str(e),
            )


class SystemStatusTool:
    """System status tool implementation."""

    @measure_execution_time
    async def execute(self) -> SystemStatusOutput:
        """Execute system_status tool."""
        try:
            logger.info("Fetching system status")

            status_data = get_system_status()
            data = SystemStatus(**status_data)

            return SystemStatusOutput(
                success=True,
                data=data,
            )
        except Exception as e:
            logger.error(f"System status tool error: {str(e)}")
            return SystemStatusOutput(
                success=False,
                error=str(e),
            )


# Tool registry
TOOLS_REGISTRY: Dict[str, Any] = {
    "get_weather": {
        "name": "get_weather",
        "description": "Fetch weather information for a city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name",
                },
                "unit": {
                    "type": "string",
                    "enum": ["metric", "imperial", "kelvin"],
                    "description": "Temperature unit",
                    "default": "metric",
                },
            },
            "required": ["city"],
        },
        "handler": WeatherTool(),
    },
    "github_user_lookup": {
        "name": "github_user_lookup",
        "description": "Lookup GitHub user profile and repositories",
        "input_schema": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "GitHub username",
                },
                "include_repos": {
                    "type": "boolean",
                    "description": "Include repositories",
                    "default": True,
                },
            },
            "required": ["username"],
        },
        "handler": GitHubUserLookupTool(),
    },
    "summarize_text": {
        "name": "summarize_text",
        "description": "Summarize text content",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to summarize",
                },
                "max_length": {
                    "type": "integer",
                    "description": "Maximum length of summary",
                    "default": 100,
                },
                "language": {
                    "type": "string",
                    "description": "Language code",
                    "default": "en",
                },
            },
            "required": ["text"],
        },
        "handler": SummarizeTextTool(),
    },
    "system_status": {
        "name": "system_status",
        "description": "Get system status including CPU, memory, and uptime",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
        "handler": SystemStatusTool(),
    },
}
