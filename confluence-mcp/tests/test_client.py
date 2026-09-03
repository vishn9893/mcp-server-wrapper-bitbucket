import httpx
import pytest
from confluence_mcp.client import ConfluenceClient, ConfluenceError
from confluence_mcp.config import Settings
from confluence_mcp import tools

def settings(**kwargs): return Settings(url="https://site.atlassian.net", email="a@b.test", token="secret", **kwargs)
def dc_settings(**kwargs): return Settings(url="https://confluence.example.local", personal_token="secret", **kwargs)

@pytest.mark.asyncio
async def test_page_path_and_basic_auth():
    seen = []
    def handler(request): seen.append(request); return httpx.Response(200, json={"results": []})
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://site.atlassian.net/wiki/api/v2") as http:
        async with ConfluenceClient(settings(), http) as client: await tools.list_pages(client, "123")
    assert str(seen[0].url).endswith("/spaces/123/pages?limit=25")
    assert seen[0].headers["authorization"].startswith("Basic ")

@pytest.mark.asyncio
async def test_error_contains_message():
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r: httpx.Response(403, json={"message": "Forbidden"})), base_url="https://site.atlassian.net/wiki/api/v2") as http:
        async with ConfluenceClient(settings(), http) as client:
            with pytest.raises(ConfluenceError, match="Forbidden"): await client.get("/spaces/1")

@pytest.mark.asyncio
async def test_data_center_uses_legacy_content_endpoint_and_bearer_auth():
    seen = []
    def handler(request): seen.append(request); return httpx.Response(200, json={"results": []})
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://confluence.example.local/rest/api/2") as http:
        async with ConfluenceClient(dc_settings(), http) as client: await tools.list_pages(client, "DOCS")
    assert str(seen[0].url).endswith("/content?type=page&limit=25&expand=version%2Cspace&spaceKey=DOCS")
    assert seen[0].headers["authorization"] == "Bearer secret"
