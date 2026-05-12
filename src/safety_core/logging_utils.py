import logging
import sys
import json
import os
from typing import Any, Dict, Optional

try:
    import google.cloud.logging
    from google.cloud.logging.handlers import CloudLoggingHandler
    GCP_LOGGING_AVAILABLE = True
except ImportError:
    GCP_LOGGING_AVAILABLE = False

class JsonFormatter(logging.Formatter):
    """
    Standardizes logs into a JSON format compatible with Cloud Logging.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
            "timestamp": self.formatTime(record, self.datefmt),
            "module": record.module,
            "line": record.lineno,
        }
        
        # Merge structured data if provided in 'extra'
        if hasattr(record, "extra_data"):
            log_entry.update(record.extra_data)
            
        return json.dumps(log_entry)

def setup_cloud_logging() -> Optional[google.cloud.logging.Client]:
    """
    Attempts to initialize the Google Cloud Logging client.
    """
    if not GCP_LOGGING_AVAILABLE:
        return None
    
    try:
        client = google.cloud.logging.Client()
        client.setup_logging()
        return client
    except Exception:
        # Fallback to standard logging if ADC is not configured
        return None

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger with support for JSON and Cloud Logging.
    """
    logger = logging.getLogger(name)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    
    if not logger.handlers:
        # Default JSON Stream Handler for stdout (ideal for GKE/Cloud Run)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        
    return logger

def log_event(logger: logging.Logger, level: int, message: str, extra: Optional[Dict[str, Any]] = None):
    """
    Helper to log structured events with extra metadata.
    """
    if extra:
        logger.log(level, message, extra={"extra_data": extra})
    else:
        logger.log(level, message)
