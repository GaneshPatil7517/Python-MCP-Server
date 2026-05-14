"""
Pydantic schemas for MCP tools.
Defines input/output validation for all tools.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, validator


class ToolInputBase(BaseModel):
    """Base class for tool inputs."""

    pass


class GetWeatherInput(ToolInputBase):
    """Schema for get_weather tool input."""

    city: str = Field(..., description="City name", min_length=1, max_length=100)
    unit: str = Field(default="metric", description="Temperature unit (metric, imperial, kelvin)")

    @validator("unit")
    def validate_unit(cls, v):
        valid_units = {"metric", "imperial", "kelvin"}
        if v not in valid_units:
            raise ValueError(f"Unit must be one of {valid_units}")
        return v


class WeatherData(BaseModel):
    """Weather data response."""

    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    description: str
    wind_speed: float
    cloudiness: int


class GetWeatherOutput(BaseModel):
    """Schema for get_weather tool output."""

    success: bool
    data: Optional[WeatherData] = None
    error: Optional[str] = None


class GitHubUserLookupInput(ToolInputBase):
    """Schema for github_user_lookup tool input."""

    username: str = Field(
        ..., description="GitHub username", min_length=1, max_length=39, pattern=r"^[a-zA-Z0-9-]+$"
    )
    include_repos: bool = Field(default=True, description="Include repositories")


class Repository(BaseModel):
    """GitHub repository information."""

    name: str
    url: str
    description: Optional[str] = None
    stars: int
    language: Optional[str] = None
    is_fork: bool


class GitHubUserData(BaseModel):
    """GitHub user profile data."""

    username: str
    name: Optional[str] = None
    bio: Optional[str] = None
    url: str
    followers: int
    following: int
    public_repos: int
    avatar_url: str
    repositories: Optional[List[Repository]] = None


class GitHubUserLookupOutput(BaseModel):
    """Schema for github_user_lookup tool output."""

    success: bool
    data: Optional[GitHubUserData] = None
    error: Optional[str] = None


class SummarizeTextInput(ToolInputBase):
    """Schema for summarize_text tool input."""

    text: str = Field(..., description="Text to summarize", min_length=10, max_length=10000)
    max_length: int = Field(default=100, description="Maximum length of summary", ge=10, le=500)
    language: str = Field(default="en", description="Language code")


class SummarizeTextOutput(BaseModel):
    """Schema for summarize_text tool output."""

    success: bool
    summary: Optional[str] = None
    original_length: Optional[int] = None
    summary_length: Optional[int] = None
    error: Optional[str] = None


class SystemStatus(BaseModel):
    """System status information."""

    cpu_percent: float
    memory_percent: float
    memory_available_gb: float
    uptime_seconds: float
    timestamp: str


class SystemStatusOutput(BaseModel):
    """Schema for system_status tool output."""

    success: bool
    data: Optional[SystemStatus] = None
    error: Optional[str] = None


class ToolDefinition(BaseModel):
    """MCP Tool definition."""

    name: str
    description: str
    input_schema: Dict[str, Any]


class ToolResponse(BaseModel):
    """Generic tool response."""

    tool_name: str
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[float] = None
