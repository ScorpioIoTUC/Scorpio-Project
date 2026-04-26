from dataclasses import dataclass


@dataclass
class LoggingClientInitArgs:
    """Initialization arguments for the logging client facade.

    Attributes:
        logger_name: Name of the logger instance.
        client_name: Concrete backend client implementation. Defaults to "python_logging".
    """

    logger_name: str = "app"
    client_name: str = "python_logging"
