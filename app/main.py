"""
Main FastAPI application with MCP server implementation.
Entry point for the MCP server.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError as PydanticValidationError

from app.config.settings import get_settings
from app.core.logging_config import setup_logging
from app.core.exceptions import MCPException
from app.middleware.auth import (
    AuthenticationMiddleware,
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
    RequestLoggingMiddleware,
)
from app.tools.implementations import TOOLS_REGISTRY
from app.resources.implementations import ResourceProvider, RESOURCES_REGISTRY
from app.prompts.implementations import PromptProvider, PROMPTS_REGISTRY
from app.utils.helpers import generate_request_id, format_success_response, format_error_response
from app.schemas.tools import ToolResponse
import time

# Setup logging
settings = get_settings()
logger = setup_logging(
    log_level=settings.log_level,
    log_file=settings.log_file,
    json_format=settings.log_json,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("MCP Server starting up...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Authentication enabled: {settings.enable_auth}")
    logger.info(f"Rate limiting enabled: {settings.rate_limit_enabled}")
    yield
    logger.info("MCP Server shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan,
)


# Add middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Exception handlers
@app.exception_handler(MCPException)
async def mcp_exception_handler(request: Request, exc: MCPException):
    """Handle MCP exceptions."""
    logger.error(f"MCP Exception: {exc.message}", extra={"extra_data": exc.to_dict()})
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


@app.exception_handler(PydanticValidationError)
async def validation_exception_handler(request: Request, exc: PydanticValidationError):
    """Handle Pydantic validation errors."""
    logger.error(f"Validation error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=format_error_response(
            error_code="VALIDATION_ERROR",
            message="Request validation failed",
            details={"errors": exc.errors()},
        ),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_error_response(
            error_code="INTERNAL_ERROR",
            message="Internal server error",
        ),
    )


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return format_success_response(
        {
            "status": "healthy",
            "timestamp": time.time(),
        }
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with server information."""
    return format_success_response(
        {
            "title": settings.api_title,
            "version": settings.api_version,
            "description": settings.api_description,
            "documentation": "/docs",
            "openapi": "/openapi.json",
        }
    )


# ==================== TOOLS ENDPOINTS ====================


@app.get("/api/tools", tags=["Tools"])
async def list_tools():
    """List all available MCP tools."""
    logger.info("Listing available tools")

    tools = [
        {
            "name": tool_info["name"],
            "description": tool_info["description"],
            "input_schema": tool_info["input_schema"],
        }
        for tool_info in TOOLS_REGISTRY.values()
    ]

    return format_success_response(
        {
            "total": len(tools),
            "tools": tools,
        }
    )


@app.post("/api/tools/execute", tags=["Tools"], response_model=ToolResponse)
async def execute_tool(request: Request):
    """Execute an MCP tool."""
    try:
        body = await request.json()
        tool_name = body.get("tool")
        tool_input = body.get("input", {})

        logger.info(f"Executing tool: {tool_name}")

        if tool_name not in TOOLS_REGISTRY:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool '{tool_name}' not found",
            )

        tool_info = TOOLS_REGISTRY[tool_name]
        handler = tool_info["handler"]

        start_time = time.time()

        # Execute tool based on type
        if tool_name == "system_status":
            result = await handler.execute()
        elif tool_name in ["get_weather", "summarize_text"]:
            from app.schemas.tools import GetWeatherInput, SummarizeTextInput

            input_schema = GetWeatherInput if tool_name == "get_weather" else SummarizeTextInput
            validated_input = input_schema(**tool_input)
            result = await handler.execute(validated_input)
        elif tool_name == "github_user_lookup":
            from app.schemas.tools import GitHubUserLookupInput

            validated_input = GitHubUserLookupInput(**tool_input)
            result = await handler.execute(validated_input)

        execution_time = (time.time() - start_time) * 1000

        logger.info(f"Tool executed successfully: {tool_name} ({execution_time:.2f}ms)")

        return ToolResponse(
            tool_name=tool_name,
            success=result.success,
            result=result.dict(),
            execution_time_ms=execution_time,
        )

    except Exception as e:
        logger.error(f"Tool execution failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# ==================== RESOURCES ENDPOINTS ====================


@app.get("/api/resources", tags=["Resources"])
async def list_resources():
    """List all available MCP resources."""
    logger.info("Listing available resources")

    resources = [
        {
            "uri": resource_info["uri"],
            "name": resource_info["name"],
            "description": resource_info["description"],
            "mime_type": resource_info["mime_type"],
        }
        for resource_info in RESOURCES_REGISTRY.values()
    ]

    return format_success_response(
        {
            "total": len(resources),
            "resources": resources,
        }
    )


@app.get("/api/resources/{resource_name}", tags=["Resources"])
async def get_resource(resource_name: str):
    """Get a specific MCP resource."""
    logger.info(f"Fetching resource: {resource_name}")

    if resource_name not in RESOURCES_REGISTRY:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource '{resource_name}' not found",
        )

    resource_info = RESOURCES_REGISTRY[resource_name]
    provider_method = resource_info["provider"]

    # Get resource data from provider
    if provider_method == "api_documentation":
        data = ResourceProvider.get_api_documentation()
    elif provider_method == "server_status":
        data = ResourceProvider.get_server_status()
    elif provider_method == "project_information":
        data = ResourceProvider.get_project_information()
    elif provider_method == "usage_guide":
        data = ResourceProvider.get_usage_guide()
    elif provider_method == "tools_list":
        data = ResourceProvider.get_tools_list()
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unknown resource provider",
        )

    return format_success_response(
        {
            "resource_uri": resource_info["uri"],
            "resource_name": resource_name,
            "data": data,
        }
    )


# ==================== PROMPTS ENDPOINTS ====================


@app.get("/api/prompts", tags=["Prompts"])
async def list_prompts():
    """List all available MCP prompts."""
    logger.info("Listing available prompts")

    prompts = [
        {
            "name": prompt_info["name"],
            "description": prompt_info["description"],
        }
        for prompt_info in PROMPTS_REGISTRY.values()
    ]

    return format_success_response(
        {
            "total": len(prompts),
            "prompts": prompts,
        }
    )


@app.get("/api/prompts/{prompt_name}", tags=["Prompts"])
async def get_prompt(prompt_name: str):
    """Get a specific MCP prompt."""
    logger.info(f"Fetching prompt: {prompt_name}")

    if prompt_name not in PROMPTS_REGISTRY:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt '{prompt_name}' not found",
        )

    prompt_info = PROMPTS_REGISTRY[prompt_name]
    provider_method = prompt_info["provider"]

    # Get prompt data from provider
    if provider_method == "debugging_assistant":
        data = PromptProvider.get_debugging_assistant_prompt()
    elif provider_method == "code_review_assistant":
        data = PromptProvider.get_code_review_assistant_prompt()
    elif provider_method == "architecture_explanation":
        data = PromptProvider.get_architecture_explanation_prompt()
    elif provider_method == "api_documentation":
        data = PromptProvider.get_api_documentation_prompt()
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unknown prompt provider",
        )

    return format_success_response(
        {
            "prompt_name": prompt_name,
            "data": data,
        }
    )


# ==================== STATUS ENDPOINTS ====================


@app.get("/api/status", tags=["Status"])
async def server_status():
    """Get server status and metrics."""
    logger.info("Getting server status")
    return format_success_response(ResourceProvider.get_server_status())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
        reload=settings.debug,
    )
