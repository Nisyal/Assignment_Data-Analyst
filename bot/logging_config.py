"""Logging configuration for the trading bot.

Sets up a rotating file handler and a console handler with consistent
formatting. API secrets are never logged.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOG_DIR / "app.log"

LOG_FORMAT = "[%(asctime)s] [%(levelname)-8s] %(name)s — %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

MAX_BYTES = 5 * 1024 * 1024  # 5 MB per log file
BACKUP_COUNT = 3


def setup_logging(level: int = logging.DEBUG) -> None:
    """Configure root logger with rotating file and console handlers.

    Args:
        level: The minimum log level to capture. Defaults to DEBUG.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # Rotating file handler — captures everything
    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler — shows WARNING and above only
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Avoid adding duplicate handlers on repeated imports
    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger.

    Args:
        name: The logger name, typically __name__ of the calling module.

    Returns:
        A configured Logger instance.
    """
    return logging.getLogger(name)
