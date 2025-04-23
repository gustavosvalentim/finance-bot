import logging
import os


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(asctime)s - %(message)s')
    
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if os.getenv("DEBUG") == "True" else logging.INFO)
    logger.addHandler(handler)

    return logger
