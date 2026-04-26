from abc import ABC, abstractmethod


class LoggingClientContract(ABC):
    @abstractmethod
    def debug(self, message: str) -> None:
        """Log a debug level message."""
        pass

    @abstractmethod
    def info(self, message: str) -> None:
        """Log an info level message."""
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        """Log a warning level message."""
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """Log an error level message."""
        pass

    @abstractmethod
    def critical(self, message: str) -> None:
        """Log a critical level message."""
        pass
