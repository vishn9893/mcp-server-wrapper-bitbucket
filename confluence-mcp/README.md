# Confluence Cloud MCP

Native async Python MCP server for Confluence Cloud REST API v2 and Confluence Server/Data Center REST API v2. Cloud uses `CONFLUENCE_EMAIL` + `CONFLUENCE_TOKEN`; Data Center uses `CONFLUENCE_PERSONAL_TOKEN` or `CONFLUENCE_USERNAME` + `CONFLUENCE_PASSWORD`.

Configure the matching variables and run:

```bash
uv sync
uv run confluence-mcp
```

The URL determines the API mode automatically: `*.atlassian.net` uses Cloud endpoints, while other hosts use Data Center endpoints. Exposes page, space, child, label, and comment tools. Build with `uv build`; publish with `UV_PUBLISH_TOKEN=pypi-... uv publish`. The package name is `confluence-mcp-atlassian`.
