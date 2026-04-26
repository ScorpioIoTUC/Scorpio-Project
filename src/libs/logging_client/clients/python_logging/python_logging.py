import logging
import sys

from src.libs.logging_client.logging_client_contract import LoggingClientContract
from src.libs.logging_client.types.logging_client_types import LoggingClientInitArgs


class PythonLoggingClient(LoggingClientContract):
    """Concrete logging client using Python's built-in logging module."""

    _LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    _DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, args: LoggingClientInitArgs) -> None:
        """
        Initialize the Python logging client.

        Args:
            args: Initialization arguments containing logger_name and client_name.
        """
        self.logger = logging.getLogger(args.logger_name)
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            self._configure_stdout_handler()

    def _configure_stdout_handler(self) -> None:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(self._LOG_FORMAT, datefmt=self._DATE_FORMAT)
        )
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def debug(self, message: str) -> None:
        """Log a debug level message."""
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Log an info level message."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning level message."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error level message."""
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """Log a critical level message."""
        self.logger.critical(message)
