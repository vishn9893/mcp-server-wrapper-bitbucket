from __future__ import annotations
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, Awaitable, Callable
from mcp.server.fastmcp import FastMCP
from .client import ConfluenceClient
from .config import get_settings
from . import tools

@asynccontextmanager
async def _client():
    async with ConfluenceClient(get_settings()) as client: yield client

def _api(fn: Callable[..., Awaitable[Any]]):
    @wraps(fn)
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        async with _client() as client: return await fn(client, *args, **kwargs)
    return wrapped

mcp = FastMCP("confluence-mcp", instructions="Confluence Cloud REST API v2 tools.")

@mcp.tool()
async def list_pages(space_id: str | None = None, title: str | None = None, limit: int = 25) -> Any: return await _api(tools.list_pages)(space_id, title, limit)
@mcp.tool()
async def get_page(page_id: str, include_body: bool = True) -> Any: return await _api(tools.get_page)(page_id, include_body)
@mcp.tool()
async def create_page(space_id: str, title: str, body: str, parent_id: str | None = None) -> Any: return await _api(tools.create_page)(space_id, title, body, parent_id)
@mcp.tool()
async def update_page(page_id: str, title: str, body: str, version: int, status: str = "current") -> Any: return await _api(tools.update_page)(page_id, title, body, version, status)
@mcp.tool()
async def delete_page(page_id: str) -> Any: return await _api(tools.delete_page)(page_id)
@mcp.tool()
async def list_spaces(limit: int = 25) -> Any: return await _api(tools.list_spaces)(limit)
@mcp.tool()
async def get_space(space_id: str) -> Any: return await _api(tools.get_space)(space_id)
@mcp.tool()
async def list_page_children(page_id: str, limit: int = 25) -> Any: return await _api(tools.list_children)(page_id, limit)
@mcp.tool()
async def list_page_labels(page_id: str, limit: int = 25) -> Any: return await _api(tools.list_labels)(page_id, limit)
@mcp.tool()
async def list_page_comments(page_id: str, limit: int = 25) -> Any: return await _api(tools.list_comments)(page_id, limit)
@mcp.tool()
async def add_page_comment(page_id: str, body: str) -> Any: return await _api(tools.add_comment)(page_id, body)

def main() -> None:
    transport = get_settings().transport
    if transport not in {"stdio", "sse", "streamable-http"}: raise ValueError("CONFLUENCE_TRANSPORT must be stdio, sse, or streamable-http")
    get_settings().validate_auth(); mcp.run(transport=transport)

if __name__ == "__main__": main()
