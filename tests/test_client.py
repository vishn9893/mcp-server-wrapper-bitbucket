import httpx
import pytest
import respx

from bitbucket_mcp.client import BitbucketClient
from bitbucket_mcp.config import Settings


@pytest.mark.asyncio
@respx.mock
async def test_get_pull_request():
    route = respx.get("https://bitbucket.example.com/rest/api/1.0/projects/PROJ/repos/repo/pull-requests/7").mock(
        return_value=httpx.Response(200, json={"id": 7, "version": 3})
    )
    client = BitbucketClient(Settings("https://bitbucket.example.com", token="secret"))
    try:
        result = await client.get_pull_request("PROJ", "repo", 7)
    finally:
        await client.close()
    assert result["id"] == 7
    assert route.called
