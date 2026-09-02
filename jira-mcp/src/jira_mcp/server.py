from __future__ import annotations
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, Awaitable, Callable
from mcp.server.fastmcp import FastMCP
from .client import JiraClient
from .config import get_settings
from . import tools

@asynccontextmanager
async def _client():
    async with JiraClient(get_settings()) as client: yield client
def _api(fn: Callable[..., Awaitable[Any]]):
    @wraps(fn)
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        async with _client() as client: return await fn(client, *args, **kwargs)
    return wrapped
mcp = FastMCP("jira-mcp", instructions="Jira Cloud REST API v3 tools.")

@mcp.tool()
async def search_issues(jql: str, max_results: int = 50, fields: list[str] | None = None) -> Any: return await _api(tools.search_issues)(jql, max_results, fields)
@mcp.tool()
async def get_issue(issue_key: str, fields: list[str] | None = None) -> Any: return await _api(tools.get_issue)(issue_key, fields)
@mcp.tool()
async def create_issue(project_key: str, issue_type: str, summary: str, description: str | None = None, extra_fields: dict[str, Any] | None = None) -> Any: return await _api(tools.create_issue)(project_key, issue_type, summary, description, extra_fields)
@mcp.tool()
async def update_issue(issue_key: str, fields: dict[str, Any]) -> Any: return await _api(tools.update_issue)(issue_key, fields)
@mcp.tool()
async def delete_issue(issue_key: str) -> Any: return await _api(tools.delete_issue)(issue_key)
@mcp.tool()
async def add_comment(issue_key: str, body: str) -> Any: return await _api(tools.add_comment)(issue_key, body)
@mcp.tool()
async def list_comments(issue_key: str, limit: int = 50) -> Any: return await _api(tools.list_comments)(issue_key, limit)
@mcp.tool()
async def get_transitions(issue_key: str) -> Any: return await _api(tools.get_transitions)(issue_key)
@mcp.tool()
async def transition_issue(issue_key: str, transition_id: str, fields: dict[str, Any] | None = None) -> Any: return await _api(tools.transition_issue)(issue_key, transition_id, fields)
@mcp.tool()
async def assign_issue(issue_key: str, account_id: str | None = None) -> Any: return await _api(tools.assign_issue)(issue_key, account_id)
@mcp.tool()
async def list_projects(limit: int = 50) -> Any: return await _api(tools.list_projects)(limit)
@mcp.tool()
async def get_project(project_key: str) -> Any: return await _api(tools.get_project)(project_key)
@mcp.tool()
async def list_issue_types() -> Any: return await _api(tools.list_issue_types)()

def main() -> None:
    transport = get_settings().transport
    if transport not in {"stdio", "sse", "streamable-http"}: raise ValueError("JIRA_TRANSPORT must be stdio, sse, or streamable-http")
    get_settings().validate_auth(); mcp.run(transport=transport)
if __name__ == "__main__": main()
