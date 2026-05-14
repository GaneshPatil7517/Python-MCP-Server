"""
Pydantic schemas for MCP resources.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class ResourceMetadata(BaseModel):
    """Metadata for a resource."""

    name: str
    description: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    version: str = "1.0.0"
    tags: List[str] = []


class APIDocumentationResource(BaseModel):
    """API documentation resource."""

    title: str
    description: str
    endpoints: List[Dict[str, Any]]
    base_url: str
    authentication: str


class ServerStatusResource(BaseModel):
    """Server status resource."""

    status: str
    uptime_seconds: float
    version: str
    environment: str
    timestamp: str


class ProjectInformationResource(BaseModel):
    """Project information resource."""

    name: str
    description: str
    version: str
    author: str
    repository: str
    documentation_url: str


class UsageGuideResource(BaseModel):
    """Usage guide resource."""

    title: str
    sections: List[Dict[str, str]]
    examples: List[str]


class ToolListResource(BaseModel):
    """Available tools list resource."""

    total: int
    tools: List[Dict[str, Any]]


class ResourceDefinition(BaseModel):
    """MCP Resource definition."""

    uri: str
    name: str
    description: str
    mime_type: str = "application/json"


class ResourceResponse(BaseModel):
    """Generic resource response."""

    resource_uri: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
