"""
Pydantic schemas for MCP prompts.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class PromptArgument(BaseModel):
    """Argument for a prompt."""

    name: str
    description: str
    required: bool = True


class PromptDefinition(BaseModel):
    """MCP Prompt definition."""

    name: str
    description: str
    arguments: List[PromptArgument]


class DebuggingAssistantPrompt(BaseModel):
    """Debugging assistant prompt."""

    system_prompt: str
    user_context: Optional[str] = None
    error_message: Optional[str] = None
    code_snippet: Optional[str] = None
    suggested_approach: Optional[str] = None


class CodeReviewAssistantPrompt(BaseModel):
    """Code review assistant prompt."""

    system_prompt: str
    code: str
    language: str
    focus_areas: List[str] = []
    severity_threshold: str = "medium"


class ArchitectureExplanationPrompt(BaseModel):
    """Architecture explanation prompt."""

    system_prompt: str
    component: str
    depth_level: str = "intermediate"
    include_diagram: bool = False


class APIDocumentationPrompt(BaseModel):
    """API documentation assistant prompt."""

    system_prompt: str
    endpoint: str
    method: str
    request_schema: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None


class PromptResponse(BaseModel):
    """Generic prompt response."""

    prompt_name: str
    success: bool
    content: Optional[str] = None
    error: Optional[str] = None
