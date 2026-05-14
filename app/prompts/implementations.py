"""
MCP Prompts implementation.
Provides predefined prompts for various AI assistant tasks.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger("app")


class PromptProvider:
    """Provides MCP prompts."""

    @staticmethod
    def get_debugging_assistant_prompt() -> Dict[str, Any]:
        """Get debugging assistant prompt."""
        return {
            "name": "debugging-assistant",
            "description": "Helps debug code and troubleshoot issues",
            "system_prompt": """You are a debugging expert assistant. Your role is to help developers:
- Analyze error messages and stack traces
- Identify root causes of issues
- Suggest fixes and workarounds
- Provide debugging strategies
- Explain why issues occur

When debugging:
1. Ask clarifying questions if needed
2. Analyze error patterns
3. Consider edge cases
4. Provide step-by-step solutions
5. Suggest prevention strategies""",
            "arguments": [
                {
                    "name": "error_message",
                    "description": "The error message or exception",
                    "required": True,
                },
                {
                    "name": "code_snippet",
                    "description": "Relevant code snippet",
                    "required": False,
                },
                {
                    "name": "context",
                    "description": "Additional context about the issue",
                    "required": False,
                },
            ],
        }

    @staticmethod
    def get_code_review_assistant_prompt() -> Dict[str, Any]:
        """Get code review assistant prompt."""
        return {
            "name": "code-review-assistant",
            "description": "Provides code review and suggestions",
            "system_prompt": """You are a senior code reviewer. Your role is to:
- Review code quality
- Identify bugs and potential issues
- Suggest improvements for readability and performance
- Check adherence to best practices
- Provide constructive feedback

When reviewing code:
1. Check for syntax and logic errors
2. Evaluate code structure and organization
3. Assess performance implications
4. Review error handling
5. Check for security vulnerabilities
6. Suggest naming improvements
7. Recommend refactoring opportunities
8. Highlight positive aspects""",
            "arguments": [
                {
                    "name": "code",
                    "description": "Code to review",
                    "required": True,
                },
                {
                    "name": "language",
                    "description": "Programming language",
                    "required": True,
                },
                {
                    "name": "focus_areas",
                    "description": "Specific areas to focus on (performance, security, readability, etc.)",
                    "required": False,
                },
            ],
        }

    @staticmethod
    def get_architecture_explanation_prompt() -> Dict[str, Any]:
        """Get architecture explanation prompt."""
        return {
            "name": "architecture-explanation",
            "description": "Explains system architecture and design patterns",
            "system_prompt": """You are a system architect. Your role is to:
- Explain system design and architecture
- Describe component interactions
- Discuss design patterns used
- Explain scalability considerations
- Discuss tradeoffs and decisions

When explaining architecture:
1. Provide clear overview
2. Describe main components
3. Explain data flows
4. Discuss communication patterns
5. Address scalability concerns
6. Explain security considerations
7. Suggest improvements
8. Include diagrams when helpful""",
            "arguments": [
                {
                    "name": "component",
                    "description": "System component to explain",
                    "required": True,
                },
                {
                    "name": "depth_level",
                    "description": "Explanation depth (beginner, intermediate, advanced)",
                    "required": False,
                },
                {
                    "name": "include_diagram",
                    "description": "Include ASCII diagram in explanation",
                    "required": False,
                },
            ],
        }

    @staticmethod
    def get_api_documentation_prompt() -> Dict[str, Any]:
        """Get API documentation prompt."""
        return {
            "name": "api-documentation",
            "description": "Generates API documentation",
            "system_prompt": """You are an API documentation expert. Your role is to:
- Generate clear API documentation
- Explain endpoints and their purposes
- Document request/response schemas
- Provide usage examples
- Clarify authentication and authorization
- Describe error responses

When documenting APIs:
1. Provide endpoint overview
2. List all parameters with descriptions
3. Show request/response examples
4. Document error cases
5. Explain authentication
6. Provide curl and SDK examples
7. Include rate limiting info
8. Add practical use cases""",
            "arguments": [
                {
                    "name": "endpoint",
                    "description": "API endpoint to document",
                    "required": True,
                },
                {
                    "name": "method",
                    "description": "HTTP method (GET, POST, PUT, DELETE, etc.)",
                    "required": True,
                },
                {
                    "name": "request_schema",
                    "description": "Request schema/body",
                    "required": False,
                },
                {
                    "name": "response_schema",
                    "description": "Response schema",
                    "required": False,
                },
            ],
        }


# Prompts registry
PROMPTS_REGISTRY: Dict[str, Any] = {
    "debugging-assistant": {
        "name": "debugging-assistant",
        "description": "Helps debug code and troubleshoot issues",
        "provider": "debugging_assistant",
    },
    "code-review-assistant": {
        "name": "code-review-assistant",
        "description": "Provides code review and suggestions",
        "provider": "code_review_assistant",
    },
    "architecture-explanation": {
        "name": "architecture-explanation",
        "description": "Explains system architecture and design patterns",
        "provider": "architecture_explanation",
    },
    "api-documentation": {
        "name": "api-documentation",
        "description": "Generates API documentation",
        "provider": "api_documentation",
    },
}
