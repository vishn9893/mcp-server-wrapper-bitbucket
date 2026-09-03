# Atlassian MCP Servers

Native asynchronous Python MCP servers for Bitbucket Server/Data Center, Jira Cloud, and Confluence Cloud. Each server talks directly to its product's REST API and can be installed and run independently.

## Packages

| Package | API | PyPI name | Directory |
| --- | --- | --- | --- |
| Bitbucket | Server/Data Center REST API v1.0 | `bitbucket-mcp-atlassian` | repository root |
| Jira | Cloud REST API v3 / Server-DC REST API v2 | `jira-mcp-atlassian` | [`jira-mcp/`](jira-mcp/) |
| Confluence | Cloud REST API v2 / Server-DC REST API v2 | `confluence-mcp-atlassian` | [`confluence-mcp/`](confluence-mcp/) |

The Jira and Confluence packages are self-contained projects with their own `pyproject.toml`, tests, environment example, and release metadata.

## Quick start

Install [uv](https://docs.astral.sh/uv/), configure the package you want to use, and run its MCP entrypoint.

### Bitbucket Server/Data Center

```bash
cp .env.example .env
uv sync
uv run bitbucket-mcp
```

Set `BITBUCKET_URL` and either `BITBUCKET_TOKEN` or both `BITBUCKET_USERNAME` and `BITBUCKET_PASSWORD`.

### Jira Cloud

```bash
cd jira-mcp
cp .env.example .env
uv sync
uv run jira-mcp
```

Set `JIRA_URL`, `JIRA_EMAIL`, and `JIRA_TOKEN`. The token is an Atlassian API token associated with the email address.

### Confluence Cloud

```bash
cd confluence-mcp
cp .env.example .env
uv sync
uv run confluence-mcp
```

Set `CONFLUENCE_URL`, `CONFLUENCE_EMAIL`, and `CONFLUENCE_TOKEN`.

Each server supports `stdio`, `sse`, and `streamable-http` transports through its corresponding `*_TRANSPORT` setting. TLS verification, timeout, and retry behavior are configurable through the environment files.

## MCP configuration examples

```json
{
  "mcpServers": {
    "bitbucket": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/this-repo", "bitbucket-mcp"],
      "env": {
        "BITBUCKET_URL": "https://bitbucket.example.com",
        "BITBUCKET_TOKEN": "your-token"
      }
    },
    "jira": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/this-repo/jira-mcp", "jira-mcp"],
      "env": {
        "JIRA_URL": "https://your-domain.atlassian.net",
        "JIRA_EMAIL": "you@example.com",
        "JIRA_TOKEN": "your-token"
      }
    },
    "confluence": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/this-repo/confluence-mcp", "confluence-mcp"],
      "env": {
        "CONFLUENCE_URL": "https://your-domain.atlassian.net",
        "CONFLUENCE_EMAIL": "you@example.com",
        "CONFLUENCE_TOKEN": "your-token"
      }
    }
  }
}
```

## Capabilities

Bitbucket provides projects, repositories, pull requests, comments, reviews, diffs, branches, commits, files, users, permissions, and build-status tools.

Jira provides JQL issue search, issue retrieval and updates, issue creation/deletion, comments, transitions, assignments, projects, and issue types. Cloud uses ADF for rich text; Server/Data Center uses Jira wiki markup.

Confluence provides page listing, retrieval, creation, updates, deletion, spaces, child pages, labels, and comments on both Cloud and Server/Data Center.

## Development and testing

Run the existing Bitbucket tests from the repository root:

```bash
uv run pytest
```

Run the independent Atlassian Cloud test suites from their package directories:

```bash
cd confluence-mcp && uv run pytest
cd ../jira-mcp && uv run pytest
```

All tests use mocked HTTP transports and do not contact Atlassian services.

## Build and publish

Build an individual package from its directory:

```bash
cd jira-mcp
uv build
```

The root [release workflow](.github/workflows/release.yml) publishes packages through PyPI trusted publishing when matching tags are pushed:

```bash
git tag jira-v0.1.0
git push origin jira-v0.1.0

git tag confluence-v0.1.0
git push origin confluence-v0.1.0
```

Configure the `pypi` GitHub environment and trusted publishers for the repository before pushing release tags. Each release workflow uses PyPI's short-lived OIDC credential; no long-lived PyPI token is stored in GitHub.

## Architecture

```text
src/bitbucket_mcp/             Bitbucket Server/Data Center implementation
jira-mcp/src/jira_mcp/          Jira Cloud implementation
confluence-mcp/src/confluence_mcp/  Confluence Cloud implementation

Each package follows the same structure:
  client.py   async HTTP and authentication infrastructure
  config.py   pydantic-settings environment configuration
  tools.py    REST API capability functions
  server.py   FastMCP tool registration and transport entrypoint
```
