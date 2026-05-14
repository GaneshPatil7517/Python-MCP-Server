"""
Authentication middleware for API requests.
Supports API key and bearer token authentication.
"""

import logging
from typing import Optional, Callable
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.config.settings import get_settings
from app.core.exceptions import AuthenticationError

logger = logging.getLogger("app")


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Middleware for request authentication."""

    def __init__(self, app: Callable):
        super().__init__(app)
        self.settings = get_settings()

    async def dispatch(self, request: Request, call_next: Callable):
        """Process request authentication."""

        # Skip auth for health check and docs
        if request.url.path in ["/health", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)

        if not self.settings.enable_auth:
            return await call_next(request)

        try:
            auth_header = request.headers.get("Authorization")
            api_key = request.headers.get("X-API-Key")

            if not auth_header and not api_key:
                raise AuthenticationError("Missing authentication credentials")

            # Check API Key
            if api_key:
                if api_key != self.settings.api_key:
                    raise AuthenticationError("Invalid API key")

            # Check Bearer Token
            elif auth_header:
                if not auth_header.startswith("Bearer "):
                    raise AuthenticationError("Invalid authorization header format")

                token = auth_header[7:]
                if token != self.settings.bearer_token:
                    raise AuthenticationError("Invalid bearer token")

            request.state.authenticated = True
            return await call_next(request)

        except AuthenticationError as e:
            logger.warning(f"Authentication failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
            )


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting."""

    def __init__(self, app: Callable):
        super().__init__(app)
        self.settings = get_settings()
        self._requests = {}

    async def dispatch(self, request: Request, call_next: Callable):
        """Process rate limiting."""

        if not self.settings.rate_limit_enabled:
            return await call_next(request)

        client_id = request.client.host if request.client else "unknown"

        if client_id not in self._requests:
            self._requests[client_id] = []

        from datetime import datetime, timedelta

        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=1)

        # Clean old requests
        self._requests[client_id] = [
            req_time for req_time in self._requests[client_id] if req_time > cutoff
        ]

        # Check rate limit
        if len(self._requests[client_id]) >= self.settings.rate_limit_requests_per_minute:
            logger.warning(f"Rate limit exceeded for {client_id}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
                headers={"Retry-After": "60"},
            )

        self._requests[client_id].append(now)
        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers."""

    async def dispatch(self, request: Request, call_next: Callable):
        """Add security headers to response."""
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        if request.url.path in ["/docs", "/redoc"]:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' data: https://fastapi.tiangolo.com; "
                "font-src 'self' https://cdn.jsdelivr.net; "
                "connect-src 'self'; "
                "frame-ancestors 'none'"
            )
        else:
            response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging."""

    async def dispatch(self, request: Request, call_next: Callable):
        """Log request and response."""
        from time import time

        start_time = time()
        request.state.start_time = start_time

        response = await call_next(request)

        process_time = (time() - start_time) * 1000

        logger.info(
            f"{request.method} {request.url.path}",
            extra={
                "extra_data": {
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "process_time_ms": process_time,
                }
            },
        )

        response.headers["X-Process-Time"] = str(process_time)
        return response
