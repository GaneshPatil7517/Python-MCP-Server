"""
MCP Resources implementation.
Provides read-only resources like API documentation, status, etc.
"""

import logging
from typing import Dict, Any
from datetime import datetime
from app.utils.helpers import get_system_status
from app.config.settings import get_settings

logger = logging.getLogger("app")


class ResourceProvider:
    """Provides MCP resources."""

    @staticmethod
    def get_api_documentation() -> Dict[str, Any]:
        """Get API documentation resource."""
        return {
            "title": "Python MCP Server API",
            "description": "Production-ready MCP server with tools, resources, and prompts",
            "version": "1.0.0",
            "endpoints": [
                {
                    "path": "/tools",
                    "method": "GET",
                    "description": "List all available tools",
                },
                {
                    "path": "/tools/execute",
                    "method": "POST",
                    "description": "Execute a tool",
                },
                {
                    "path": "/resources",
                    "method": "GET",
                    "description": "List all available resources",
                },
                {
                    "path": "/resources/{resource_name}",
                    "method": "GET",
                    "description": "Get a specific resource",
                },
                {
                    "path": "/prompts",
                    "method": "GET",
                    "description": "List all available prompts",
                },
                {
                    "path": "/prompts/{prompt_name}",
                    "method": "GET",
                    "description": "Get a specific prompt",
                },
                {
                    "path": "/health",
                    "method": "GET",
                    "description": "Health check endpoint",
                },
            ],
            "base_url": "http://localhost:8000",
            "authentication": "API Key (X-API-Key header) or Bearer Token",
        }

    @staticmethod
    def get_server_status() -> Dict[str, Any]:
        """Get server status resource."""
        system = get_system_status()
        settings = get_settings()

        return {
            # top-level metrics for backward compatibility
            "cpu_percent": system["cpu_percent"],
            "memory_percent": system["memory_percent"],
            "status": "operational",
            "uptime_seconds": system["uptime_seconds"],
            "version": settings.api_version,
            "environment": settings.environment,
            "timestamp": datetime.utcnow().isoformat(),
            "system": {
                "cpu_percent": system["cpu_percent"],
                "memory_percent": system["memory_percent"],
                "memory_available_gb": system["memory_available_gb"],
            },
        }

    @staticmethod
    def get_project_information() -> Dict[str, Any]:
        """Get project information resource."""
        return {
            "name": "Python MCP Server",
            "description": "Production-ready MCP (Model Context Protocol) server built with FastAPI and Python",
            "version": "1.0.0",
            "author": "AI Engineering",
            "repository": "https://github.com/yourusername/python-mcp-server",
            "documentation_url": "https://github.com/yourusername/python-mcp-server/wiki",
            "features": [
                "MCP Tools for weather, GitHub lookup, text summarization, and system status",
                "MCP Resources for documentation and server information",
                "MCP Prompts for debugging, code review, and architecture explanation",
                "Async execution with proper error handling",
                "Rate limiting and authentication",
                "Structured logging and monitoring",
                "Docker support and easy deployment",
                "Redis caching support",
                "PostgreSQL database support",
            ],
        }

    @staticmethod
    def get_usage_guide() -> Dict[str, Any]:
        """Get usage guide resource."""
        return {
            "title": "MCP Server Usage Guide",
            "sections": {
                "overview": "This MCP server provides tools, resources, and prompts for AI assistants.",
                "tools": "Execute tools to perform actions like fetching weather, GitHub lookups, text summarization, and system status checks.",
                "resources": "Access read-only resources for API documentation, server status, and project information.",
                "prompts": "Use predefined prompts for debugging assistance, code review, architecture explanation, and API documentation.",
                "authentication": "Include X-API-Key header or Bearer token in Authorization header for authenticated requests.",
                "error_handling": "All responses follow consistent error format with error codes, messages, and details.",
                "rate_limiting": "Default rate limit is 60 requests per minute. Adjust via RATE_LIMIT_REQUESTS_PER_MINUTE.",
            },
            "examples": [
                {
                    "description": "Get weather",
                    "command": 'curl -H "X-API-Key: your-api-key" http://localhost:8000/api/tools/execute -X POST -d \'{"tool": "get_weather", "input": {"city": "London"}}\'',
                },
                {
                    "description": "Lookup GitHub user",
                    "command": 'curl -H "X-API-Key: your-api-key" http://localhost:8000/api/tools/execute -X POST -d \'{"tool": "github_user_lookup", "input": {"username": "torvalds"}}\'',
                },
                {
                    "description": "Summarize text",
                    "command": 'curl -H "X-API-Key: your-api-key" http://localhost:8000/api/tools/execute -X POST -d \'{"tool": "summarize_text", "input": {"text": "Your long text here"}}\'',
                },
            ],
        }

    @staticmethod
    def get_tools_list() -> Dict[str, Any]:
        """Get list of available tools resource."""
        from app.tools.implementations import TOOLS_REGISTRY

        tools = []
        for tool_name, tool_info in TOOLS_REGISTRY.items():
            tools.append(
                {
                    "name": tool_info["name"],
                    "description": tool_info["description"],
                    "input_schema": tool_info["input_schema"],
                }
            )

        return {
            "total": len(tools),
            "tools": tools,
        }


# Resources registry
RESOURCES_REGISTRY: Dict[str, Any] = {
    "api_documentation": {
        "uri": "mcp://resources/api_documentation",
        "name": "API Documentation",
        "description": "Complete API documentation for the MCP server",
        "mime_type": "application/json",
        "provider": "api_documentation",
    },
    "server_status": {
        "uri": "mcp://resources/server_status",
        "name": "Server Status",
        "description": "Current server status including system metrics",
        "mime_type": "application/json",
        "provider": "server_status",
    },
    "project_information": {
        "uri": "mcp://resources/project_information",
        "name": "Project Information",
        "description": "Project information and metadata",
        "mime_type": "application/json",
        "provider": "project_information",
    },
    "usage_guide": {
        "uri": "mcp://resources/usage_guide",
        "name": "Usage Guide",
        "description": "How to use the MCP server",
        "mime_type": "application/json",
        "provider": "usage_guide",
    },
    "tools_list": {
        "uri": "mcp://resources/tools_list",
        "name": "Tools List",
        "description": "List of all available tools",
        "mime_type": "application/json",
        "provider": "tools_list",
    },
}
