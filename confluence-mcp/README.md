# Confluence Cloud MCP

Native async Python MCP server for Confluence Cloud REST API v2. Configure `CONFLUENCE_URL`, `CONFLUENCE_EMAIL`, and `CONFLUENCE_TOKEN` (an Atlassian API token), then run:

```bash
uv sync
uv run confluence-mcp
```

Exposes page, space, child, label, and comment tools. Build with `uv build`; publish with `UV_PUBLISH_TOKEN=pypi-... uv publish`. The package name is `confluence-mcp-atlassian`.
