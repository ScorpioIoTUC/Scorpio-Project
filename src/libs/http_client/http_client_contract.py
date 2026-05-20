from abc import ABC, abstractmethod
from .types.http_client_types import HTTPRequestArgs


class HTTPClientContract(ABC):
    @abstractmethod
    async def get(self, args: HTTPRequestArgs) -> dict:
        pass

    @abstractmethod
    async def post(self, args: HTTPRequestArgs) -> dict:
        pass

    @abstractmethod
    async def put(self, args: HTTPRequestArgs) -> dict:
        pass

    @abstractmethod
    async def delete(self, args: HTTPRequestArgs) -> dict:
        pass

    @abstractmethod
    async def patch(self, args: HTTPRequestArgs) -> dict:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass
