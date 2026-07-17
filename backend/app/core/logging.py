import logging
import sys

from pythonjsonlogger.json import JsonFormatter


def configure_logging(log_level: str) -> None:
    """Configure concise JSON logs for application and request events."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level.upper())
