from __future__ import annotations

import json
from typing import Any, Mapping, Optional

import aiohttp

from src.libs.http_client.http_client_contract import HTTPClientContract
from src.libs.http_client.types.http_client_types import (
    HTTPClientInitArgs,
    HTTPRequestArgs,
)


class AioHTTPClient(HTTPClientContract):
    def __init__(self, args: HTTPClientInitArgs) -> None:
        self.client_name = args.client_name
        self.credentials = args.credentials or {}
        self._session: Optional[aiohttp.ClientSession] = None
        self._default_headers = self._build_default_headers()
        self._auth = self._build_auth()

    def _build_default_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}

        raw_headers = self.credentials.get("headers")
        if isinstance(raw_headers, Mapping):
            headers.update(
                {
                    str(key): str(value)
                    for key, value in raw_headers.items()
                    if value is not None
                }
            )

        authorization = self.credentials.get("authorization")
        if authorization is not None and "Authorization" not in headers:
            headers["Authorization"] = str(authorization)
            return headers

        token = self._extract_token()
        if token is not None and "Authorization" not in headers:
            token_prefix = str(self.credentials.get("token_prefix") or "Bearer")
            headers["Authorization"] = f"{token_prefix} {token}".strip()

        return headers

    def _extract_token(self) -> Optional[str]:
        token_keys = (
            "bearer_token",
            "api_token",
            "token",
            "access_token",
            "session_token",
        )
        for token_key in token_keys:
            token_value = self.credentials.get(token_key)
            if token_value:
                return str(token_value)
        return None

    def _build_auth(self) -> aiohttp.BasicAuth | None:
        raw_auth = self.credentials.get("auth")
        if isinstance(raw_auth, aiohttp.BasicAuth):
            return raw_auth

        if isinstance(raw_auth, Mapping):
            username = raw_auth.get("username") or raw_auth.get("user")
            password = raw_auth.get("password") or raw_auth.get("pass") or ""
            if username is not None:
                return aiohttp.BasicAuth(str(username), str(password))

        username = self.credentials.get("username") or self.credentials.get("user")
        if username is not None:
            password = (
                self.credentials.get("password") or self.credentials.get("pass") or ""
            )
            return aiohttp.BasicAuth(str(username), str(password))

        return None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            session_kwargs: dict[str, Any] = {
                "headers": self._default_headers,
            }
            if self._auth is not None:
                session_kwargs["auth"] = self._auth

            timeout_value = self.credentials.get("timeout")
            if timeout_value is not None:
                session_kwargs["timeout"] = aiohttp.ClientTimeout(
                    total=float(timeout_value)
                )

            self._session = aiohttp.ClientSession(**session_kwargs)

        return self._session

    async def _request(self, method: str, args: HTTPRequestArgs) -> dict[str, Any]:
        session = await self._get_session()

        request_headers: dict[str, Any] = dict(self._default_headers)
        if args.headers:
            request_headers.update(args.headers)

        request_kwargs: dict[str, Any] = {"headers": request_headers}
        if args.params is not None:
            request_kwargs["params"] = args.params
        if args.data is not None:
            request_kwargs["data"] = args.data
        if args.json is not None:
            request_kwargs["json"] = args.json
        if args.timeout is not None:
            request_kwargs["timeout"] = aiohttp.ClientTimeout(total=float(args.timeout))

            try:
                async with session.request(
                    method,
                    args.url,
                    **request_kwargs,
                ) as response:
                    payload = await self._read_response_payload(response)

                    return {
                        "ok": 200 <= response.status < 300,
                        "status": response.status,
                        "headers": dict(response.headers),
                        "url": str(response.url),
                        "data": payload,
                    }

            except (
                aiohttp.InvalidURL,
                aiohttp.ClientConnectorError,
                aiohttp.ServerTimeoutError,
                aiohttp.ClientError,
            ) as e:
                raise Exception(e)

    async def _read_response_payload(self, response: aiohttp.ClientResponse) -> Any:
        if response.status == 204:
            return None

        try:
            return await response.json(content_type=None)
        except (
            aiohttp.ContentTypeError,
            json.JSONDecodeError,
            UnicodeDecodeError,
            ValueError,
        ):
            text = await response.text()
            return text if text else None

    async def get(self, args: HTTPRequestArgs) -> dict:
        return await self._request("GET", args)

    async def post(self, args: HTTPRequestArgs) -> dict:
        return await self._request("POST", args)

    async def put(self, args: HTTPRequestArgs) -> dict:
        return await self._request("PUT", args)

    async def delete(self, args: HTTPRequestArgs) -> dict:
        return await self._request("DELETE", args)

    async def patch(self, args: HTTPRequestArgs) -> dict:
        return await self._request("PATCH", args)

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()
        self._session = None
