from __future__ import annotations

from typing import Any

from .client import BitbucketClient


def _page(data: Any) -> Any:
    return data.get("values", data) if isinstance(data, dict) else data


async def repositories(c: BitbucketClient, project_key: str | None = None, name: str | None = None, limit: int = 25) -> Any:
    path = f"/projects/{project_key}/repos" if project_key else "/repos"
    params = {"limit": limit, **({"name": name} if name else {})}
    return await c.get(path, params=params)

async def repository(c: BitbucketClient, project_key: str, repository_slug: str) -> Any:
    return await c.get(f"/projects/{project_key}/repos/{repository_slug}")

async def projects(c: BitbucketClient, name: str | None = None, limit: int = 25) -> Any:
    return await c.get("/projects", params={"limit": limit, **({"name": name} if name else {})})

async def project(c: BitbucketClient, project_key: str) -> Any: return await c.get(f"/projects/{project_key}")

async def create_pull_request(c: BitbucketClient, project_key: str, repository_slug: str, title: str,
                              description: str, from_branch: str, to_branch: str,
                              reviewers: list[dict[str, Any]] | None = None) -> Any:
    payload = {"title": title, "description": description,
               "fromRef": {"id": from_branch, "repository": {"slug": repository_slug, "project": {"key": project_key}}},
               "toRef": {"id": to_branch, "repository": {"slug": repository_slug, "project": {"key": project_key}}}}
    if reviewers: payload["reviewers"] = reviewers
    return await c.post(f"/projects/{project_key}/repos/{repository_slug}/pull-requests", json=payload)

async def get_pull_request(c: BitbucketClient, project_key: str, repository_slug: str, pull_request_id: int) -> Any:
    return await c.get(f"/projects/{project_key}/repos/{repository_slug}/pull-requests/{pull_request_id}")

async def update_pull_request(c: BitbucketClient, project_key: str, repository_slug: str, pull_request_id: int,
                              title: str | None = None, description: str | None = None) -> Any:
    data = await get_pull_request(c, project_key, repository_slug, pull_request_id)
    if title is not None: data["title"] = title
    if description is not None: data["description"] = description
    return await c.put(f"/projects/{project_key}/repos/{repository_slug}/pull-requests/{pull_request_id}", json=data)

async def list_pull_requests(c: BitbucketClient, project_key: str, repository_slug: str, state: str = "OPEN", limit: int = 25) -> Any:
    return await c.get(f"/projects/{project_key}/repos/{repository_slug}/pull-requests", params={"state": state, "limit": limit})

async def merge_pull_request(c: BitbucketClient, project_key: str, repository_slug: str, pull_request_id: int, version: int | None = None, strategy_id: str | None = None) -> Any:
    data = {"version": version} if version is not None else {"version": (await get_pull_request(c, project_key, repository_slug, pull_request_id))["version"]}
    if strategy_id: data["strategyId"] = strategy_id
    return await c.post(f"/projects/{project_key}/repos/{repository_slug}/pull-requests/{pull_request_id}/merge", json=data)

async def decline_pull_request(c: BitbucketClient, project_key: str, repository_slug: str, pull_request_id: int, version: int | None = None) -> Any:
    version = version if version is not None else (await get_pull_request(c, project_key, repository_slug, pull_request_id))["version"]
    return await c.post(f"/projects/{project_key}/repos/{repository_slug}/pull-requests/{pull_request_id}/decline", json={"version": version})

async def add_comment(c: BitbucketClient, project_key: str, repository_slug: str, pull_request_id: int, text: str, parent_id: int | None = None) -> Any:
    payload: dict[str, Any] = {"text": text}
    if parent_id is not None: payload["parent"] = {"id": parent_id}
    return await c.post(f"/projects/{project_key}/repos/{repository_slug}/pull-requests/{pull_request_id}/comments", json=payload)

async def get_comments(c: BitbucketClient, project_key: str, repository_slug: str, pull_request_id: int, limit: int = 100) -> Any:
    return await c.get(f"/projects/{project_key}/repos/{repository_slug}/pull-requests/{pull_request_id}/comments", params={"limit": limit})

async def get_diff(c: BitbucketClient, project_key: str, repository_slug: str, pull_request_id: int, context_lines: int = 10) -> Any:
    return await c.get(f"/projects/{project_key}/repos/{repository_slug}/pull-requests/{pull_request_id}.diff", params={"contextLines": context_lines}, accept="text/plain")

async def get_reviews(c: BitbucketClient, project_key: str, repository_slug: str, pull_request_id: int) -> Any:
    return await c.get(f"/projects/{project_key}/repos/{repository_slug}/pull-requests/{pull_request_id}/activities", params={"limit": 100})

async def branches(c: BitbucketClient, project_key: str, repository_slug: str, filter_text: str | None = None, limit: int = 50) -> Any:
    return await c.get(f"/projects/{project_key}/repos/{repository_slug}/branches", params={"limit": limit, **({"filterText": filter_text} if filter_text else {})})

async def commits(c: BitbucketClient, project_key: str, repository_slug: str, branch: str | None = None, limit: int = 25) -> Any:
    return await c.get(f"/projects/{project_key}/repos/{repository_slug}/commits", params={"limit": limit, **({"until": branch} if branch else {})})

async def commit(c: BitbucketClient, project_key: str, repository_slug: str, commit_id: str) -> Any: return await c.get(f"/projects/{project_key}/repos/{repository_slug}/commits/{commit_id}")

async def file_content(c: BitbucketClient, project_key: str, repository_slug: str, path: str, at: str = "HEAD") -> Any: return await c.get(f"/projects/{project_key}/repos/{repository_slug}/raw/{path}", params={"at": at}, accept="text/plain")

async def browse_files(c: BitbucketClient, project_key: str, repository_slug: str, path: str = "", at: str = "HEAD", limit: int = 100) -> Any: return await c.get(f"/projects/{project_key}/repos/{repository_slug}/files/{path}", params={"at": at, "limit": limit})

async def users(c: BitbucketClient, filter_text: str | None = None, limit: int = 25) -> Any: return await c.get("/users", params={"limit": limit, **({"filter": filter_text} if filter_text else {})})

async def user(c: BitbucketClient, username: str) -> Any: return await c.get(f"/users/{username}")

async def permissions(c: BitbucketClient, project_key: str | None = None, repository_slug: str | None = None) -> Any:
    if repository_slug and project_key: path = f"/projects/{project_key}/repos/{repository_slug}/permissions/users"
    elif project_key: path = f"/projects/{project_key}/permissions/users"
    else: path = "/permissions/users"
    return await c.get(path)

async def builds(c: BitbucketClient, project_key: str, repository_slug: str, commit_id: str | None = None, limit: int = 25) -> Any:
    path = f"/projects/{project_key}/repos/{repository_slug}/commits/{commit_id}/builds" if commit_id else f"/projects/{project_key}/repos/{repository_slug}/builds"
    return await c.get(path, params={"limit": limit})
