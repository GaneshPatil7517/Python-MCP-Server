"""
Central exception handling for MCP server.
Provides custom exceptions for consistent error handling.
"""

from typing import Any, Dict, Optional


class MCPException(Exception):
    """Base exception for all MCP server errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details,
        }


class ValidationError(MCPException):
    """Raised when validation fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400,
            details=details,
        )


class AuthenticationError(MCPException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=401,
        )


class AuthorizationError(MCPException):
    """Raised when user lacks required permissions."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=403,
        )


class NotFoundError(MCPException):
    """Raised when resource is not found."""

    def __init__(self, resource: str, identifier: str):
        message = f"{resource} '{identifier}' not found"
        super().__init__(
            message=message,
            error_code="NOT_FOUND",
            status_code=404,
            details={"resource": resource, "identifier": identifier},
        )


class RateLimitError(MCPException):
    """Raised when rate limit is exceeded."""

    def __init__(self, retry_after: int):
        super().__init__(
            message="Rate limit exceeded",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details={"retry_after": retry_after},
        )


class APIError(MCPException):
    """Raised when external API call fails."""

    def __init__(
        self,
        message: str,
        api_name: str,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code="API_ERROR",
            status_code=502,
            details={"api": api_name, **(details or {})},
        )


class TimeoutError(MCPException):
    """Raised when operation times out."""

    def __init__(self, operation: str, timeout_seconds: float):
        super().__init__(
            message=f"Operation '{operation}' timed out after {timeout_seconds}s",
            error_code="TIMEOUT",
            status_code=504,
            details={"operation": operation, "timeout_seconds": timeout_seconds},
        )


class ConfigurationError(MCPException):
    """Raised when configuration is invalid."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            status_code=500,
            details=details,
        )
