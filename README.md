# Atlassian MCP Servers

Native asynchronous Python MCP servers for Bitbucket Server/Data Center, Jira Cloud, and Confluence Cloud. Each server talks directly to its product's REST API and can be installed and run independently.

## Packages

| Package | API | PyPI name | Directory |
| --- | --- | --- | --- |
| Bitbucket | Server/Data Center REST API v1.0 | `bitbucket-mcp-atlassian` | repository root |
| Jira | Cloud REST API v3 | `jira-mcp-atlassian` | [`jira-mcp/`](jira-mcp/) |
| Confluence | Cloud REST API v2 | `confluence-mcp-atlassian` | [`confluence-mcp/`](confluence-mcp/) |

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

Jira provides JQL issue search, issue retrieval and updates, issue creation/deletion, comments, transitions, assignments, projects, and issue types. Plain-text descriptions and comments are converted to Atlassian Document Format.

Confluence provides page listing, retrieval, creation, updates, deletion, spaces, child pages, labels, and comments.

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

The root [Atlassian release workflow](.github/workflows/release-atlassian.yml) publishes packages through PyPI trusted publishing when matching tags are pushed:

```bash
git tag jira-v0.1.0
git push origin jira-v0.1.0

git tag confluence-v0.1.0
git push origin confluence-v0.1.0
```

Configure the `pypi` GitHub environment and trusted publishers for the repository before pushing release tags. The existing Bitbucket release workflow continues to publish the root package from `v*` tags.

## Install and run

Install [uv](https://docs.astral.sh/uv/), copy `.env.example` to `.env`, and set the Bitbucket URL and credentials:

```bash
cp .env.example .env
uv sync
uv run bitbucket-mcp
```

Use a personal access token with `BITBUCKET_TOKEN`, or set both `BITBUCKET_USERNAME` and `BITBUCKET_PASSWORD`. `BITBUCKET_URL` is the Bitbucket web base URL, for example `https://bitbucket.example.com` (the client appends `/rest/api/1.0`). Set `BITBUCKET_VERIFY_TLS=false` only for a deliberately trusted test certificate. `BITBUCKET_TIMEOUT`, `BITBUCKET_MAX_RETRIES`, and `BITBUCKET_TRANSPORT` (`stdio`, `sse`, or `streamable-http`) are also supported.

Example stdio MCP configuration:

```json
{
  "mcpServers": {
    "bitbucket": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/mcp-server-wrapper-bitbucket", "bitbucket-mcp"],
      "env": {"BITBUCKET_URL": "https://bitbucket.example.com", "BITBUCKET_TOKEN": "your-token"}
    }
  }
}
```

## Tools

The server currently exposes 23 tools, organized by capability:

- Projects and repositories: `list_projects`, `get_project`, `list_repositories`, `get_repository`
- Pull requests: `create_pull_request`, `get_pull_request`, `list_pull_requests`, `update_pull_request`, `merge_pull_request`, `decline_pull_request`
- Pull-request discussion and review: `add_comment`, `get_comments`, `get_diff`, `get_reviews`
- Source history: `list_branches`, `list_commits`, `get_commit`, `get_file`, `browse_files`
- Users and access: `list_users`, `get_user`, `list_permissions`
- Builds and CI: `list_builds`

All calls use Bitbucket Server/Data Center REST API v1.0 paths and return the API's JSON (or text for diffs and files), preserving pagination fields where Bitbucket supplies them. Write operations are limited to pull-request creation, updates, merge/decline, and comments; no delete tools are exposed.

## Development and testing

```bash
uv sync
uv run pytest
```

Tests use mocked `httpx.AsyncClient` responses and never contact Bitbucket. The reusable client handles bearer-token or basic authentication, TLS verification, timeouts, retries for transient responses, JSON/text responses, and useful API errors.

## Build and publish with uv

The project is a standard Python package and can be built with uv:

```bash
uv build
```

This creates a wheel and source distribution in `dist/`. After configuring a PyPI API token, publish them with:

```bash
export UV_PUBLISH_TOKEN="pypi-your-token"
uv publish
```

`uv publish` uploads to PyPI by default. Use `--publish-url` for a private package index. This project publishes as `bitbucket-mcp-atlassian`; the version in `pyproject.toml` must be incremented for each release. Publishing is intentionally not performed by the development/test commands.

### GitHub Actions Trusted Publishing

The repository includes `.github/workflows/release.yml`. Configure the PyPI publisher for repository `vishn9893/mcp-server-wrapper-bitbucket`, workflow `release.yml`, and GitHub environment `pypi`. The workflow publishes only when a `v*` tag is pushed and uses PyPI's short-lived OIDC credential.

## Architecture

```text
src/bitbucket_mcp/
  client.py   async HTTP and authentication infrastructure
  config.py   pydantic-settings environment configuration
  tools.py    REST API capability functions
  server.py   FastMCP tool registration and transport entrypoint
```
