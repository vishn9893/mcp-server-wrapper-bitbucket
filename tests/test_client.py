import httpx
import pytest

from bitbucket_mcp.client import BitbucketClient, BitbucketError
from bitbucket_mcp.config import Settings
from bitbucket_mcp import tools


def settings(**kwargs):
    return Settings(url="https://bb.example", token="secret", **kwargs)


@pytest.mark.asyncio
async def test_client_uses_bearer_auth_and_api_prefix():
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(200, json={"values": [{"slug": "demo"}]})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url="https://bb.example/rest/api/1.0") as http:
        async with BitbucketClient(settings(), http) as client:
            result = await tools.repositories(client, "PROJ")
    assert result["values"][0]["slug"] == "demo"
    assert str(requests[0].url).endswith("/projects/PROJ/repos?limit=25")
    assert requests[0].headers["authorization"] == "Bearer secret"


@pytest.mark.asyncio
async def test_pull_request_payload_and_path():
    seen = {}

    def handler(request):
        seen["method"] = request.method
        seen["url"] = str(request.url)
        seen["json"] = request.read().decode()
        return httpx.Response(201, json={"id": 7, "title": "Improve"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://bb.example/rest/api/1.0") as http:
        async with BitbucketClient(settings(), http) as client:
            result = await tools.create_pull_request(client, "PROJ", "repo", "Improve", "desc", "feature", "main")
    assert result["id"] == 7
    assert seen["method"] == "POST"
    assert seen["url"].endswith("/projects/PROJ/repos/repo/pull-requests")
    assert '"id":"feature"' in seen["json"] and '"id":"main"' in seen["json"]


@pytest.mark.asyncio
async def test_text_diff_response():
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(200, text="diff --git a/a b/a")), base_url="https://bb.example/rest/api/1.0") as http:
        async with BitbucketClient(settings(), http) as client:
            result = await tools.get_diff(client, "P", "r", 4)
    assert result.startswith("diff --git")


@pytest.mark.asyncio
async def test_api_error_contains_server_message():
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(403, json={"errors": [{"message": "Forbidden"}]})), base_url="https://bb.example/rest/api/1.0") as http:
        async with BitbucketClient(settings(), http) as client:
            with pytest.raises(BitbucketError, match="Forbidden"):
                await client.get("/projects/P")
