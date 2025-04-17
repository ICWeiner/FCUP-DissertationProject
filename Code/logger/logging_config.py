import logging
from pathlib import Path

def setup_logging():
    """Centralized logging configuration"""
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    log_file = Path(__file__).parent.parent / "app.log"  # Goes in project root
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Special configuration for specific libraries if needed
    #logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    #logging.getLogger("httpx").setLevel(logging.WARNING)