from __future__ import annotations

import asyncio
from collections.abc import Mapping
from typing import Any

import httpx

from .config import Settings


class BitbucketError(RuntimeError):
    def __init__(self, status_code: int, message: str, details: Any = None):
        super().__init__(f"Bitbucket API returned {status_code}: {message}")
        self.status_code, self.message, self.details = status_code, message, details


class BitbucketClient:
    """Small, reusable async REST client for Bitbucket Server/Data Center 1.0."""

    def __init__(self, settings: Settings, http: httpx.AsyncClient | None = None):
        self.settings = settings
        self._http = http
        self._owns_http = http is None

    async def __aenter__(self) -> "BitbucketClient":
        if self._http is None:
            auth = (self.settings.username, self.settings.password) if self.settings.username else None
            headers = {"Authorization": f"Bearer {self.settings.token}"} if self.settings.token else {}
            self._http = httpx.AsyncClient(base_url=self.settings.api_url, auth=auth, headers=headers,
                                           verify=self.settings.verify_tls, timeout=self.settings.timeout,
                                           follow_redirects=True)
        return self

    async def __aexit__(self, *exc: object) -> None:
        if self._owns_http and self._http:
            await self._http.aclose()

    async def request(self, method: str, path: str, *, params: Mapping[str, Any] | None = None,
                      json: Any = None, content: Any = None,
                      accept: str = "application/json") -> Any:
        if self._http is None:
            raise RuntimeError("BitbucketClient must be used as an async context manager")
        headers = {"Accept": accept}
        if self.settings.token:
            headers["Authorization"] = f"Bearer {self.settings.token}"
        if json is not None:
            headers["Content-Type"] = "application/json"
        for attempt in range(self.settings.max_retries + 1):
            try:
                basic_auth = (self.settings.username, self.settings.password) if self.settings.username else None
                response = await self._http.request(method, path, params=params, json=json,
                                                    content=content, headers=headers, auth=basic_auth)
                if response.status_code in {429, 502, 503, 504} and attempt < self.settings.max_retries:
                    await asyncio.sleep(min(2**attempt, 8))
                    continue
                if response.is_error:
                    try:
                        details = response.json()
                    except ValueError:
                        details = response.text
                    message = details.get("errors", [{}])[0].get("message", response.reason_phrase) \
                        if isinstance(details, dict) else str(details)
                    raise BitbucketError(response.status_code, message, details)
                if not response.content:
                    return None
                return response.json() if "json" in response.headers.get("content-type", "") else response.text
            except (httpx.TimeoutException, httpx.NetworkError):
                if attempt >= self.settings.max_retries:
                    raise
                await asyncio.sleep(min(2**attempt, 8))

    async def get(self, path: str, **kwargs: Any) -> Any: return await self.request("GET", path, **kwargs)
    async def post(self, path: str, **kwargs: Any) -> Any: return await self.request("POST", path, **kwargs)
    async def put(self, path: str, **kwargs: Any) -> Any: return await self.request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> Any: return await self.request("DELETE", path, **kwargs)

    async def close(self) -> None:
        if self._owns_http and self._http:
            await self._http.aclose()
