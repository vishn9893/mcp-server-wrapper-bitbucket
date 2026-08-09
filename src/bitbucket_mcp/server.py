from __future__ import annotations

from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, Awaitable, Callable

from mcp.server.fastmcp import FastMCP

from .client import BitbucketClient
from .config import get_settings
from . import tools


@asynccontextmanager
async def _client():
    async with BitbucketClient(get_settings()) as client:
        yield client


def _api(fn: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    @wraps(fn)
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        async with _client() as client:
            return await fn(client, *args, **kwargs)
    return wrapped


mcp = FastMCP("bitbucket-mcp", instructions="Bitbucket Server/Data Center REST API tools.")


@mcp.tool()
async def list_repositories(project_key: str | None = None, name: str | None = None, limit: int = 25) -> Any:
    """List repositories globally or within a project."""
    return await _api(tools.repositories)(project_key, name, limit)


@mcp.tool()
async def get_repository(project_key: str, repository_slug: str) -> Any:
    """Get repository metadata."""
    return await _api(tools.repository)(project_key, repository_slug)


@mcp.tool()
async def list_projects(name: str | None = None, limit: int = 25) -> Any:
    """List Bitbucket projects."""
    return await _api(tools.projects)(name, limit)


@mcp.tool()
async def get_project(project_key: str) -> Any:
    """Get a project by key."""
    return await _api(tools.project)(project_key)


@mcp.tool()
async def create_pull_request(project_key: str, repository_slug: str, title: str, description: str,
                              from_branch: str, to_branch: str, reviewers: list[dict[str, Any]] | None = None) -> Any:
    """Create a pull request."""
    return await _api(tools.create_pull_request)(project_key, repository_slug, title, description, from_branch, to_branch, reviewers)


@mcp.tool()
async def get_pull_request(project_key: str, repository_slug: str, pull_request_id: int) -> Any:
    """Retrieve pull-request details."""
    return await _api(tools.get_pull_request)(project_key, repository_slug, pull_request_id)


@mcp.tool()
async def list_pull_requests(project_key: str, repository_slug: str, state: str = "OPEN", limit: int = 25) -> Any:
    """List pull requests by state."""
    return await _api(tools.list_pull_requests)(project_key, repository_slug, state, limit)


@mcp.tool()
async def update_pull_request(project_key: str, repository_slug: str, pull_request_id: int,
                              title: str | None = None, description: str | None = None) -> Any:
    """Update pull-request title or description."""
    return await _api(tools.update_pull_request)(project_key, repository_slug, pull_request_id, title, description)


@mcp.tool()
async def merge_pull_request(project_key: str, repository_slug: str, pull_request_id: int,
                             version: int | None = None, strategy_id: str | None = None) -> Any:
    """Merge a pull request."""
    return await _api(tools.merge_pull_request)(project_key, repository_slug, pull_request_id, version, strategy_id)


@mcp.tool()
async def decline_pull_request(project_key: str, repository_slug: str, pull_request_id: int, version: int | None = None) -> Any:
    """Decline a pull request."""
    return await _api(tools.decline_pull_request)(project_key, repository_slug, pull_request_id, version)


@mcp.tool()
async def add_comment(project_key: str, repository_slug: str, pull_request_id: int, text: str, parent_id: int | None = None) -> Any:
    """Add a comment to a pull request."""
    return await _api(tools.add_comment)(project_key, repository_slug, pull_request_id, text, parent_id)


@mcp.tool()
async def get_comments(project_key: str, repository_slug: str, pull_request_id: int, limit: int = 100) -> Any:
    """List pull-request comments."""
    return await _api(tools.get_comments)(project_key, repository_slug, pull_request_id, limit)


@mcp.tool()
async def get_diff(project_key: str, repository_slug: str, pull_request_id: int, context_lines: int = 10) -> Any:
    """Get a pull-request diff."""
    return await _api(tools.get_diff)(project_key, repository_slug, pull_request_id, context_lines)


@mcp.tool()
async def get_reviews(project_key: str, repository_slug: str, pull_request_id: int) -> Any:
    """Get pull-request activity and review history."""
    return await _api(tools.get_reviews)(project_key, repository_slug, pull_request_id)


@mcp.tool()
async def list_branches(project_key: str, repository_slug: str, filter_text: str | None = None, limit: int = 50) -> Any:
    """List repository branches."""
    return await _api(tools.branches)(project_key, repository_slug, filter_text, limit)


@mcp.tool()
async def list_commits(project_key: str, repository_slug: str, branch: str | None = None, limit: int = 25) -> Any:
    """List commits, optionally from a branch."""
    return await _api(tools.commits)(project_key, repository_slug, branch, limit)


@mcp.tool()
async def get_commit(project_key: str, repository_slug: str, commit_id: str) -> Any:
    """Get commit metadata."""
    return await _api(tools.commit)(project_key, repository_slug, commit_id)


@mcp.tool()
async def get_file(project_key: str, repository_slug: str, path: str, at: str = "HEAD") -> Any:
    """Read a file at a branch, tag, or commit."""
    return await _api(tools.file_content)(project_key, repository_slug, path, at)


@mcp.tool()
async def browse_files(project_key: str, repository_slug: str, path: str = "", at: str = "HEAD", limit: int = 100) -> Any:
    """Browse repository files."""
    return await _api(tools.browse_files)(project_key, repository_slug, path, at, limit)


@mcp.tool()
async def list_users(filter_text: str | None = None, limit: int = 25) -> Any:
    """Search or list Bitbucket users."""
    return await _api(tools.users)(filter_text, limit)


@mcp.tool()
async def get_user(username: str) -> Any:
    """Get a Bitbucket user."""
    return await _api(tools.user)(username)


@mcp.tool()
async def list_permissions(project_key: str | None = None, repository_slug: str | None = None) -> Any:
    """List user permissions at the global, project, or repository scope."""
    return await _api(tools.permissions)(project_key, repository_slug)


@mcp.tool()
async def list_builds(project_key: str, repository_slug: str, commit_id: str | None = None, limit: int = 25) -> Any:
    """List build statuses from Bitbucket Server's build-status API."""
    return await _api(tools.builds)(project_key, repository_slug, commit_id, limit)


def main() -> None:
    """Run the MCP server over stdio (or BITBUCKET_TRANSPORT when supported)."""
    transport = get_settings().transport
    if transport not in {"stdio", "sse", "streamable-http"}:
        raise ValueError("BITBUCKET_TRANSPORT must be stdio, sse, or streamable-http")
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
