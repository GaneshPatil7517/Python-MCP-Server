"""
Structured logging configuration for the MCP server.
Provides consistent logging across all modules.
"""

import json
import logging
import logging.config
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        
        if hasattr(record, "extra_data"):
            log_data["extra"] = record.extra_data
        
        return json.dumps(log_data, default=str)


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = True,
) -> logging.Logger:
    """
    Configure logging for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        json_format: Whether to use JSON formatting
    
    Returns:
        Configured logger instance
    """
    
    handlers: Dict[str, Any] = {
        "console": {
            "class": "logging.StreamHandler",
            "level": log_level,
            "formatter": "json" if json_format else "standard",
            "stream": "ext://sys.stdout",
        }
    }
    
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": log_level,
            "formatter": "json" if json_format else "standard",
            "filename": log_file,
            "maxBytes": 10485760,
            "backupCount": 5,
        }
    
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
            "json": {
                "()": JSONFormatter,
            },
        },
        "handlers": handlers,
        "root": {
            "level": log_level,
            "handlers": list(handlers.keys()),
        },
        "loggers": {
            "app": {"level": log_level, "propagate": True},
            "uvicorn": {"level": "INFO", "propagate": False},
            "uvicorn.access": {"level": "INFO", "propagate": False},
        },
    }
    
    logging.config.dictConfig(config)
    return logging.getLogger("app")


class LogContext:
    """Context manager for adding context to logs."""
    
    def __init__(self, **context: Any):
        self.context = context
        self.logger = logging.getLogger("app")
    
    def __enter__(self):
        for key, value in self.context.items():
            logging.currentframe().f_locals[key] = value
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
