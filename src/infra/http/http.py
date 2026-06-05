from src.libs.http_client import HTTPClient, HTTPClientInitArgs, HTTPRequestArgs

CLIENT_NAME = "aiohttp_client"
TIMEOUT = 30


class HTTP:
    def __init__(self, url: str, credentials: dict = {}) -> None:
        self.client = HTTPClient(
            HTTPClientInitArgs(client_name=CLIENT_NAME, credentials=credentials)
        )
        self.url = url

    async def get(
        self,
        headers: dict | None = None,
        params: dict | None = None,
        data: dict | str | None = None,
        json: dict | None = None,
    ) -> dict:
        return await self.client.get(
            HTTPRequestArgs(
                url=self.url,
                headers=headers or {},
                params=params or {},
                data=data,
                json=json,
                timeout=TIMEOUT,
            )
        )

    async def post(
        self,
        headers: dict | None = None,
        params: dict | None = None,
        data: dict | str | None = None,
        json: dict | None = None,
    ) -> dict:
        return await self.client.post(
            HTTPRequestArgs(
                url=self.url,
                headers=headers or {},
                params=params or {},
                data=data,
                json=json,
                timeout=TIMEOUT,
            )
        )

    async def patch(
        self,
        headers: dict | None = None,
        params: dict | None = None,
        data: dict | str | None = None,
        json: dict | None = None,
    ) -> dict:
        return await self.client.patch(
            HTTPRequestArgs(
                url=self.url,
                headers=headers or {},
                params=params or {},
                data=data,
                json=json,
                timeout=TIMEOUT,
            )
        )

    async def delete(
        self,
        headers: dict | None = None,
        params: dict | None = None,
        data: dict | str | None = None,
        json: dict | None = None,
    ) -> dict:
        return await self.client.delete(
            HTTPRequestArgs(
                url=self.url,
                headers=headers or {},
                params=params or {},
                data=data,
                json=json,
                timeout=TIMEOUT,
            )
        )

    async def put(
        self,
        headers: dict | None = None,
        params: dict | None = None,
        data: dict | str | None = None,
        json: dict | None = None,
    ) -> dict:
        return await self.client.put(
            HTTPRequestArgs(
                url=self.url,
                headers=headers or {},
                params=params or {},
                data=data,
                json=json,
                timeout=TIMEOUT,
            )
        )
