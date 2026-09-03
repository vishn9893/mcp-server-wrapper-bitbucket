# Jira Cloud MCP

Native async Python MCP server for Jira Cloud REST API v3 and Jira Server/Data Center REST API v2. Cloud uses `JIRA_EMAIL` + `JIRA_TOKEN`; Data Center uses `JIRA_PERSONAL_TOKEN` or `JIRA_USERNAME` + `JIRA_PASSWORD`.

Configure the matching variables and run:

```bash
uv sync
uv run jira-mcp
```

The URL determines the API mode automatically: `*.atlassian.net` uses Cloud endpoints, while other hosts use Data Center endpoints. Exposes JQL search, issue CRUD, comments, transitions, assignment, project, and issue-type tools. Jira descriptions and comments use ADF in Cloud and wiki markup strings in Data Center. Build with `uv build`; publish with `UV_PUBLISH_TOKEN=pypi-... uv publish`. The package name is `jira-mcp-atlassian`.
