from __future__ import annotations
import asyncio
from collections.abc import Mapping
from typing import Any
import httpx
from .config import Settings

class JiraError(RuntimeError):
    def __init__(self, status_code: int, message: str, details: Any = None):
        super().__init__(f"Jira API returned {status_code}: {message}")
        self.status_code, self.message, self.details = status_code, message, details

class JiraClient:
    def __init__(self, settings: Settings, http: httpx.AsyncClient | None = None): self.settings, self._http, self._owns_http = settings, http, http is None
    async def __aenter__(self) -> "JiraClient":
        if self._http is None:
            auth = (self.settings.email, self.settings.token) if self.settings.is_cloud else ((self.settings.username, self.settings.password) if self.settings.username else None)
            self._http = httpx.AsyncClient(base_url=self.settings.api_url, auth=auth, headers=self._auth_headers(), verify=self.settings.verify_tls, timeout=self.settings.timeout, follow_redirects=True)
        return self
    async def __aexit__(self, *exc: object) -> None:
        if self._owns_http and self._http: await self._http.aclose()
    async def request(self, method: str, path: str, *, params: Mapping[str, Any] | None = None, json: Any = None) -> Any:
        if self._http is None: raise RuntimeError("JiraClient must be used as an async context manager")
        headers = {"Accept": "application/json", **self._auth_headers()}
        auth = (self.settings.email, self.settings.token) if self.settings.is_cloud else ((self.settings.username, self.settings.password) if self.settings.username else None)
        for attempt in range(self.settings.max_retries + 1):
            try:
                response = await self._http.request(method, path, params=params, json=json, headers=headers, auth=auth)
                if response.status_code in {429, 502, 503, 504} and attempt < self.settings.max_retries:
                    await asyncio.sleep(min(2**attempt, 8)); continue
                if response.is_error:
                    try: details = response.json()
                    except ValueError: details = response.text
                    if isinstance(details, dict): message = "; ".join(details.get("errorMessages", [])) or str(details.get("errors", details))
                    else: message = str(details)
                    raise JiraError(response.status_code, message, details)
                return response.json() if response.content else None
            except (httpx.TimeoutException, httpx.NetworkError):
                if attempt >= self.settings.max_retries: raise
                await asyncio.sleep(min(2**attempt, 8))
    async def get(self, path: str, **kwargs: Any) -> Any: return await self.request("GET", path, **kwargs)
    async def post(self, path: str, **kwargs: Any) -> Any: return await self.request("POST", path, **kwargs)
    async def put(self, path: str, **kwargs: Any) -> Any: return await self.request("PUT", path, **kwargs)
    async def delete(self, path: str, **kwargs: Any) -> Any: return await self.request("DELETE", path, **kwargs)

    def _auth_headers(self) -> dict[str, str]:
        if not self.settings.is_cloud:
            token = self.settings.personal_token or (self.settings.token if not self.settings.username else None)
            if token: return {"Authorization": f"Bearer {token}"}
        return {}
