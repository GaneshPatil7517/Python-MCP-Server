"""
Database models for the MCP server.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import JSON

Base = declarative_base()


class APIRequest(Base):
    """Model for API request logging."""

    __tablename__ = "api_requests"

    id = Column(String(36), primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    method = Column(String(10))
    path = Column(String(255))
    status_code = Column(Integer)
    response_time_ms = Column(Float)
    user_id = Column(String(36), nullable=True, index=True)
    ip_address = Column(String(45))
    user_agent = Column(String(512), nullable=True)
    request_body = Column(JSON, nullable=True)
    response_body = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)


class APIKey(Base):
    """Model for API keys."""

    __tablename__ = "api_keys"

    id = Column(String(36), primary_key=True)
    name = Column(String(255))
    key = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    rate_limit = Column(Integer, nullable=True)
    scopes = Column(JSON, default=list)
    last_used = Column(DateTime, nullable=True)


class ToolExecution(Base):
    """Model for tool execution logging."""

    __tablename__ = "tool_executions"

    id = Column(String(36), primary_key=True)
    tool_name = Column(String(255), index=True)
    status = Column(String(20))
    input_data = Column(JSON)
    output_data = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    execution_time_ms = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    user_id = Column(String(36), nullable=True)


class CacheEntry(Base):
    """Model for cache entries."""

    __tablename__ = "cache_entries"

    id = Column(String(255), primary_key=True)
    key = Column(String(512), unique=True, index=True)
    value = Column(JSON)
    expires_at = Column(DateTime, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    hit_count = Column(Integer, default=0)


class AuditLog(Base):
    """Model for audit logging."""

    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True)
    action = Column(String(255))
    resource_type = Column(String(100))
    resource_id = Column(String(255), nullable=True)
    user_id = Column(String(36), nullable=True)
    ip_address = Column(String(45))
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String(20))
