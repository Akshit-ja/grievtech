import logging
import os
from logging.handlers import RotatingFileHandler

# ------------------------------
# Paths
# ------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# ------------------------------
# Logger Configuration
# ------------------------------

def setup_logging():
    """
    Configure application-wide logging.
    Logs to both console and rotating file.
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs
    if logger.handlers:
        return logger

    # ------------------------------
    # Log Format
    # ------------------------------
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ------------------------------
    # Console Handler
    # ------------------------------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # ------------------------------
    # Rotating File Handler
    # ------------------------------
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # ------------------------------
    # Add Handlers
    # ------------------------------
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger