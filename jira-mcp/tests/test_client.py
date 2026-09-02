import base64
import httpx
import pytest
from jira_mcp.client import JiraClient, JiraError
from jira_mcp.config import Settings
from jira_mcp import tools

def settings(**kwargs): return Settings(url="https://site.atlassian.net", email="a@b.test", token="secret", **kwargs)

@pytest.mark.asyncio
async def test_search_uses_jql_endpoint_and_auth():
    seen = []
    def handler(request): seen.append(request); return httpx.Response(200, json={"issues": []})
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://site.atlassian.net/rest/api/3") as http:
        async with JiraClient(settings(), http) as client: await tools.search_issues(client, "project = DEMO")
    assert str(seen[0].url).endswith("/search/jql")
    assert seen[0].headers["authorization"] == "Basic " + base64.b64encode(b"a@b.test:secret").decode()
    assert 'project = DEMO' in seen[0].content.decode()

@pytest.mark.asyncio
async def test_error_contains_message():
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r: httpx.Response(400, json={"errorMessages": ["Bad JQL"]})), base_url="https://site.atlassian.net/rest/api/3") as http:
        async with JiraClient(settings(), http) as client:
            with pytest.raises(JiraError, match="Bad JQL"): await client.get("/issue/DEMO-1")
