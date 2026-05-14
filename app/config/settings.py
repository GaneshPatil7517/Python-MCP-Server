"""
Configuration settings for the MCP server.
Uses environment variables with validation.
"""

from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment")

    # API Configuration
    api_title: str = Field(default="Python MCP Server", description="API title")
    api_version: str = Field(default="1.0.0", description="API version")
    api_description: str = Field(
        default="Production-ready MCP server with tools, resources, and prompts"
    )

    # Security
    secret_key: str = Field(default="dev-secret-key-change-in-production")
    api_key: str = Field(default="", description="API key for authentication")
    bearer_token: str = Field(default="", description="Bearer token for authentication")
    enable_auth: bool = Field(default=True, description="Enable authentication")

    # CORS
    cors_origins: list = Field(default=["*"], description="CORS allowed origins")
    cors_allow_credentials: bool = Field(default=True)
    cors_allow_methods: list = Field(default=["*"])
    cors_allow_headers: list = Field(default=["*"])

    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True)
    rate_limit_requests_per_minute: int = Field(default=60)
    rate_limit_requests_per_hour: int = Field(default=1000)

    # External APIs
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    weather_api_key: Optional[str] = Field(default=None, description="Weather API key")
    github_token: Optional[str] = Field(default=None, description="GitHub token")

    # Database
    database_url: Optional[str] = Field(default="sqlite:///./mcp.db", description="Database URL")

    # Redis
    redis_url: Optional[str] = Field(default=None, description="Redis URL for caching")

    # Logging
    log_level: str = Field(default="INFO")
    log_file: Optional[str] = Field(default=None)
    log_json: bool = Field(default=True)

    # Timeouts (seconds)
    http_timeout: int = Field(default=30)
    api_call_timeout: int = Field(default=60)

    # Performance
    cache_enabled: bool = Field(default=True)
    cache_ttl: int = Field(default=3600)

    class Config:
        env_file = ".env"
        case_sensitive = False

    @validator("environment")
    def validate_environment(cls, v):
        valid = {"development", "staging", "production"}
        if v not in valid:
            raise ValueError(f"Environment must be one of {valid}")
        return v

    @validator("api_version")
    def validate_version(cls, v):
        if not isinstance(v, str) or not v.count(".") >= 1:
            raise ValueError("Version must be in format X.Y.Z")
        return v

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached)."""
    return Settings()
