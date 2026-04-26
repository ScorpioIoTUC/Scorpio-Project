from src.libs.logging_client import LoggingClient, LoggingClientInitArgs


class Logging:
    """Facade for the logging client library."""

    def __init__(
        self, logger_name: str = "app", client_name: str = "python_logging"
    ) -> None:
        """
        Initialize the logging facade.

        Args:
            logger_name: Name of the logger instance. Defaults to "app".
            client_name: Concrete backend client implementation. Defaults to "python_logging".
        """
        args = LoggingClientInitArgs(logger_name=logger_name, client_name=client_name)
        self._client = LoggingClient(args)

    def debug(self, message: str) -> None:
        """Log a debug level message."""
        self._client.debug(message)

    def info(self, message: str) -> None:
        """Log an info level message."""
        self._client.info(message)

    def warning(self, message: str) -> None:
        """Log a warning level message."""
        self._client.warning(message)

    def error(self, message: str) -> None:
        """Log an error level message."""
        self._client.error(message)

    def critical(self, message: str) -> None:
        """Log a critical level message."""
        self._client.critical(message)
