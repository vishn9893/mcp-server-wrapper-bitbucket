# Bitbucket Server MCP

Native Python MCP server for Bitbucket Server and Data Center. It uses the Bitbucket REST API directly with a single self-contained runtime.

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
