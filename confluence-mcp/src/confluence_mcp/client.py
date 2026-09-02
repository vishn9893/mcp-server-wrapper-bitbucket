from __future__ import annotations
import asyncio
from collections.abc import Mapping
from typing import Any
import httpx
from .config import Settings


class ConfluenceError(RuntimeError):
    def __init__(self, status_code: int, message: str, details: Any = None):
        super().__init__(f"Confluence API returned {status_code}: {message}")
        self.status_code, self.message, self.details = status_code, message, details


class ConfluenceClient:
    def __init__(self, settings: Settings, http: httpx.AsyncClient | None = None):
        self.settings, self._http, self._owns_http = settings, http, http is None

    async def __aenter__(self) -> "ConfluenceClient":
        if self._http is None:
            self._http = httpx.AsyncClient(base_url=self.settings.api_url,
                auth=(self.settings.email, self.settings.token), verify=self.settings.verify_tls,
                timeout=self.settings.timeout, follow_redirects=True)
        return self

    async def __aexit__(self, *exc: object) -> None:
        if self._owns_http and self._http:
            await self._http.aclose()

    async def request(self, method: str, path: str, *, params: Mapping[str, Any] | None = None,
                      json: Any = None) -> Any:
        if self._http is None:
            raise RuntimeError("ConfluenceClient must be used as an async context manager")
        headers = {"Accept": "application/json"}
        auth = (self.settings.email, self.settings.token) if self.settings.email else None
        for attempt in range(self.settings.max_retries + 1):
            try:
                response = await self._http.request(method, path, params=params, json=json, headers=headers, auth=auth)
                if response.status_code in {429, 502, 503, 504} and attempt < self.settings.max_retries:
                    await asyncio.sleep(min(2**attempt, 8)); continue
                if response.is_error:
                    try: details = response.json()
                    except ValueError: details = response.text
                    message = details.get("message", response.reason_phrase) if isinstance(details, dict) else str(details)
                    raise ConfluenceError(response.status_code, message, details)
                return response.json() if response.content else None
            except (httpx.TimeoutException, httpx.NetworkError):
                if attempt >= self.settings.max_retries: raise
                await asyncio.sleep(min(2**attempt, 8))

    async def get(self, path: str, **kwargs: Any) -> Any: return await self.request("GET", path, **kwargs)
    async def post(self, path: str, **kwargs: Any) -> Any: return await self.request("POST", path, **kwargs)
    async def put(self, path: str, **kwargs: Any) -> Any: return await self.request("PUT", path, **kwargs)
    async def delete(self, path: str, **kwargs: Any) -> Any: return await self.request("DELETE", path, **kwargs)
