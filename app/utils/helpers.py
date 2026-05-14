"""
Utility functions for the MCP server.
"""

import uuid
import logging
import psutil
from typing import Dict, Any
from datetime import datetime
from functools import wraps
from time import time

logger = logging.getLogger("app")


def generate_request_id() -> str:
    """Generate unique request ID."""
    return str(uuid.uuid4())


def get_system_status() -> Dict[str, Any]:
    """Get current system status."""
    boot_time = psutil.boot_time()
    uptime = time() - boot_time

    memory = psutil.virtual_memory()

    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": memory.percent,
        "memory_available_gb": memory.available / (1024**3),
        "uptime_seconds": uptime,
        "timestamp": datetime.utcnow().isoformat(),
    }


def sanitize_input(value: str, max_length: int = 1000) -> str:
    """Sanitize user input."""
    if not isinstance(value, str):
        value = str(value)

    # Remove null bytes
    value = value.replace("\x00", "")

    # Limit length
    value = value[:max_length]

    return value.strip()


def measure_execution_time(func):
    """Decorator to measure function execution time."""

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            execution_time = (time() - start_time) * 1000
            logger.info(f"Function {func.__name__} executed in {execution_time:.2f}ms")

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            execution_time = (time() - start_time) * 1000
            logger.info(f"Function {func.__name__} executed in {execution_time:.2f}ms")

    # Return async wrapper if function is async
    if hasattr(func, "__call__"):
        import inspect

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return sync_wrapper


def format_error_response(
    error_code: str,
    message: str,
    details: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Format error response."""
    return {
        "success": False,
        "error": error_code,
        "message": message,
        "details": details or {},
        "timestamp": datetime.utcnow().isoformat(),
    }


def format_success_response(data: Any) -> Dict[str, Any]:
    """Format success response."""
    return {
        "success": True,
        "data": data,
        "timestamp": datetime.utcnow().isoformat(),
    }
