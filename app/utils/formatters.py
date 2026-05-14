"""
Additional helper functions for MCP server utilities.
"""

import hashlib
import json
from typing import Any, Dict


def generate_hash(data: Any) -> str:
    """Generate SHA256 hash of data."""
    data_str = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(data_str.encode()).hexdigest()


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate string to max length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def format_bytes(bytes_value: float) -> str:
    """Format bytes to human-readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def parse_pagination_params(skip: int = 0, limit: int = 10) -> Dict[str, int]:
    """Validate and return pagination parameters."""
    skip = max(0, skip)
    limit = max(1, min(limit, 100))  # Max 100 per page
    return {"skip": skip, "limit": limit}


def chunks(items: list, size: int):
    """Split list into chunks."""
    for i in range(0, len(items), size):
        yield items[i : i + size]
