from abc import ABC, abstractmethod
from typing import Any, Dict
from .types.dbms_client_types import DBExecuteArgs, DBInitializeArgs


class DbmsClientContract(ABC):
    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the database."""
        pass

    @abstractmethod
    async def initialize(self, args: DBInitializeArgs) -> None:
        """Run schema / initialization SQL statements."""
        pass

    @abstractmethod
    async def execute(self, args: DBExecuteArgs) -> Dict[str, Any]:
        """Execute a query and return a result dictionary."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the database connection."""
        pass
