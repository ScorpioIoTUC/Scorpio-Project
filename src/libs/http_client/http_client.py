from typing import Any
from .http_client_contract import HTTPClientContract
from .types.http_client_types import HTTPClientInitArgs, HTTPRequestArgs
from .clients.aiohttp_client import AioHTTPClient


class HTTPClient(HTTPClientContract):
    CLIENTS = {"aiohttp_client"}

    def __init__(self, args: HTTPClientInitArgs) -> None:
        if args.client_name not in HTTPClient.CLIENTS:
            msg = f"Unsupported client {args.client_name}"
            raise KeyError(msg)
        if args.client_name == "aiohttp_client":
            self.client_obj = AioHTTPClient(args)
        self.client_name = args.client_name

    async def get(self, args: HTTPRequestArgs) -> dict[str, Any]:
        return await self.client_obj.get(args)

    async def post(self, args: HTTPRequestArgs) -> dict[str, Any]:
        return await self.client_obj.post(args)

    async def put(self, args: HTTPRequestArgs) -> dict[str, Any]:
        return await self.client_obj.put(args)

    async def delete(self, args: HTTPRequestArgs) -> dict[str, Any]:
        return await self.client_obj.delete(args)

    async def patch(self, args: HTTPRequestArgs) -> dict[str, Any]:
        return await self.client_obj.patch(args)

    async def close(self) -> None:
        return await self.client_obj.close()
