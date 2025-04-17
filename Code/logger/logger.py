import logging
from .logging_config import setup_logging

# Initialize logging configuration
setup_logging()

def get_logger(name: str) -> logging.Logger:
    """Get a pre-configured logger instance"""
    return logging.getLogger(name)