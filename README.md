# Bitbucket MCP Server — Native Python

A self-contained Model Context Protocol (MCP) server for Bitbucket Server/Data Center, implemented entirely in Python.

The previous version was a FastAPI wrapper around a Node.js MCP server. This version removes that architecture: there is no npm build, Node.js runtime, or JavaScript submodule.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Bitbucket Server/Data Center
- A Bitbucket access token, or username/password

## Quick start

```bash
uv sync
export BITBUCKET_URL=https://bitbucket.example.com
export BITBUCKET_TOKEN=your-token
uv run bitbucket-mcp
```

The default MCP transport is stdio, making it suitable for MCP clients that launch local servers.

## Configuration

| Variable | Required | Description |
|---|---|---|
| `BITBUCKET_URL` | yes | Base URL of Bitbucket Server/Data Center |
| `BITBUCKET_TOKEN` | one auth method | Bearer access token |
| `BITBUCKET_USERNAME` | one auth method | Basic-auth username |
| `BITBUCKET_PASSWORD` | one auth method | Basic-auth password |
| `BITBUCKET_VERIFY_SSL` | no | Set to `false` only when TLS verification must be disabled |

## MCP tools

- `create_pull_request`
- `get_pull_request`
- `merge_pull_request`
- `decline_pull_request`
- `add_comment`
- `get_diff`
- `get_reviews`

All tools call Bitbucket's REST API directly from Python.

## Development

```bash
uv sync --dev
uv run pytest
uv run bitbucket-mcp
```

The project uses a `src/` layout and keeps runtime dependencies in `pyproject.toml` so `uv.lock` can provide reproducible environments.

## Architecture

```text
MCP client
   |
   | MCP / stdio
   v
bitbucket_mcp.server
   |
   v
bitbucket_mcp.client
   |
   | HTTPS REST API
   v
Bitbucket Server / Data Center
```

No Node.js process or subprocess bridge is involved.

## License

Apache-2.0
