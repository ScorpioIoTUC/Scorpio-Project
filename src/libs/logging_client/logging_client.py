from .clients.python_logging.python_logging import PythonLoggingClient
from .logging_client_contract import LoggingClientContract
from .types.logging_client_types import LoggingClientInitArgs


class LoggingClient(LoggingClientContract):
    """Main logging client using adapter pattern to select concrete implementations."""

    CLIENTS = {"python_logging"}

    def __init__(self, args: LoggingClientInitArgs) -> None:
        """
        Initialize the logging client.

        Args:
            args: Initialization arguments specifying client_name and logger_name.

        Raises:
            KeyError: If the specified client_name is not supported.
        """
        if args.client_name not in LoggingClient.CLIENTS:
            msg = f"Unsupported client {args.client_name}"
            raise KeyError(msg)
        if args.client_name == "python_logging":
            self.client_obj = PythonLoggingClient(args)
        self.client_name = args.client_name

    def debug(self, message: str) -> None:
        """Log a debug level message."""
        return self.client_obj.debug(message)

    def info(self, message: str) -> None:
        """Log an info level message."""
        return self.client_obj.info(message)

    def warning(self, message: str) -> None:
        """Log a warning level message."""
        return self.client_obj.warning(message)

    def error(self, message: str) -> None:
        """Log an error level message."""
        return self.client_obj.error(message)

    def critical(self, message: str) -> None:
        """Log a critical level message."""
        return self.client_obj.critical(message)
