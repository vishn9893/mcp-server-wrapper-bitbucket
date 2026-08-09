from fastmcp import FastMCP

from .client import BitbucketClient
from .config import Settings

mcp = FastMCP("Bitbucket Server")
_client: BitbucketClient | None = None


def client() -> BitbucketClient:
    global _client
    if _client is None:
        _client = BitbucketClient(Settings.from_env())
    return _client


@mcp.tool()
async def create_pull_request(project: str, repository: str, title: str, from_ref: str, to_ref: str,
                              description: str = "", reviewers: list[str] | None = None) -> dict:
    """Create a pull request in Bitbucket Server/Data Center."""
    return await client().create_pull_request(project, repository, title, from_ref, to_ref, description, reviewers)


@mcp.tool()
async def get_pull_request(project: str, repository: str, pull_request_id: int) -> dict:
    """Get pull request details."""
    return await client().get_pull_request(project, repository, pull_request_id)


@mcp.tool()
async def merge_pull_request(project: str, repository: str, pull_request_id: int, version: int | None = None) -> dict:
    """Merge a pull request."""
    return await client().merge_pull_request(project, repository, pull_request_id, version)


@mcp.tool()
async def decline_pull_request(project: str, repository: str, pull_request_id: int, version: int | None = None) -> dict:
    """Decline a pull request."""
    return await client().decline_pull_request(project, repository, pull_request_id, version)


@mcp.tool()
async def add_comment(project: str, repository: str, pull_request_id: int, text: str) -> dict:
    """Add a comment to a pull request."""
    return await client().add_comment(project, repository, pull_request_id, text)


@mcp.tool()
async def get_diff(project: str, repository: str, pull_request_id: int) -> dict:
    """Get the pull request diff."""
    return await client().get_diff(project, repository, pull_request_id)


@mcp.tool()
async def get_reviews(project: str, repository: str, pull_request_id: int) -> dict:
    """Get pull request activity/review history."""
    return await client().get_reviews(project, repository, pull_request_id)


def main() -> None:
    mcp.run()
