# Jira Cloud MCP

Native async Python MCP server for Jira Cloud REST API v3. Configure `JIRA_URL`, `JIRA_EMAIL`, and `JIRA_TOKEN` (an Atlassian API token), then run:

```bash
uv sync
uv run jira-mcp
```

Exposes JQL search, issue CRUD, comments, transitions, assignment, project, and issue-type tools. Jira descriptions and comments supplied as plain text are converted to Atlassian Document Format (ADF). Build with `uv build`; publish with `UV_PUBLISH_TOKEN=pypi-... uv publish`. The package name is `jira-mcp-atlassian`.
