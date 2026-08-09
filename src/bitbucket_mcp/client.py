from typing import Any

import httpx

from .config import Settings


class BitbucketError(RuntimeError):
    """Raised when Bitbucket returns an unsuccessful response."""


class BitbucketClient:
    def __init__(self, settings: Settings):
        headers = {"Accept": "application/json"}
        auth = None
        if settings.token:
            headers["Authorization"] = f"Bearer {settings.token}"
        else:
            auth = (settings.username, settings.password)
        self._client = httpx.AsyncClient(
            base_url=f"{settings.base_url}/rest/api/1.0",
            headers=headers,
            auth=auth,
            verify=settings.verify_ssl,
            timeout=30.0,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def request(self, method: str, path: str, **kwargs: Any) -> Any:
        response = await self._client.request(method, path, **kwargs)
        if response.is_error:
            detail = response.text[:1000]
            raise BitbucketError(f"Bitbucket {response.status_code}: {detail}")
        if not response.content:
            return {"status": response.status_code}
        return response.json()

    async def create_pull_request(self, project: str, repository: str, title: str,
                                  from_ref: str, to_ref: str, description: str = "",
                                  reviewers: list[str] | None = None) -> Any:
        payload: dict[str, Any] = {
            "title": title,
            "description": description,
            "fromRef": {"id": from_ref, "repository": {"slug": repository, "project": {"key": project}}},
            "toRef": {"id": to_ref, "repository": {"slug": repository, "project": {"key": project}}},
        }
        if reviewers:
            payload["reviewers"] = [{"user": {"name": name}} for name in reviewers]
        return await self.request("POST", f"/projects/{project}/repos/{repository}/pull-requests", json=payload)

    async def get_pull_request(self, project: str, repository: str, pull_request_id: int) -> Any:
        return await self.request("GET", f"/projects/{project}/repos/{repository}/pull-requests/{pull_request_id}")

    async def merge_pull_request(self, project: str, repository: str, pull_request_id: int,
                                 version: int | None = None) -> Any:
        if version is None:
            pr = await self.get_pull_request(project, repository, pull_request_id)
            version = pr["version"]
        return await self.request("POST", f"/projects/{project}/repos/{repository}/pull-requests/{pull_request_id}/merge",
                                  json={"version": version})

    async def decline_pull_request(self, project: str, repository: str, pull_request_id: int,
                                   version: int | None = None) -> Any:
        if version is None:
            pr = await self.get_pull_request(project, repository, pull_request_id)
            version = pr["version"]
        return await self.request("POST", f"/projects/{project}/repos/{repository}/pull-requests/{pull_request_id}/decline",
                                  json={"version": version})

    async def add_comment(self, project: str, repository: str, pull_request_id: int, text: str) -> Any:
        return await self.request("POST", f"/projects/{project}/repos/{repository}/pull-requests/{pull_request_id}/comments",
                                  json={"text": text})

    async def get_diff(self, project: str, repository: str, pull_request_id: int) -> Any:
        return await self.request("GET", f"/projects/{project}/repos/{repository}/pull-requests/{pull_request_id}/diff")

    async def get_reviews(self, project: str, repository: str, pull_request_id: int) -> Any:
        return await self.request("GET", f"/projects/{project}/repos/{repository}/pull-requests/{pull_request_id}/activities",
                                  params={"limit": 1000})
