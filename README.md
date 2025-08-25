# CodeSage Core

Core Model Context Protocol (MCP) server for CodeSage, implemented with **FastMCP**.

## Features

- FastMCP-based async server
- Modular service layer for internal tools
- External MCP client integration (GitHub MCP Server)
- .env based configuration

## Quick Start

Install Python deps:

```bash
uv sync
```

Copy env file and add token:

```bash
cp .env.example .env
# Fill in GITHUB_PERSONAL_ACCESS_TOKEN (or GITHUB_TOKEN / GITHUB_PAT)
```

Run the server (stdio):

```bash
codesage-core
```

HTTP transport:

```bash
codesage-core --transport http --host 127.0.0.1 --port 8000
```

## GitHub MCP Integration

Preferred token env var: `GITHUB_PERSONAL_ACCESS_TOKEN` (fallbacks: `GITHUB_TOKEN`, `GITHUB_PAT`).

Spawn strategy priority:

1. `GITHUB_MCP_COMMAND` override
2. Docker (`docker run ghcr.io/github/github-mcp-server stdio`)
3. Binary (`github-mcp-server stdio` if in PATH)

Config env vars:

- `GITHUB_TOOLSETS` (e.g. repos,pull_requests or all)
- `GITHUB_DYNAMIC_TOOLSETS=1` enable dynamic discovery
- `GITHUB_READ_ONLY=1` read-only mode
- `GITHUB_HOST` enterprise host override
- `GITHUB_MCP_MODE` force docker | binary

If no valid mode found a stub response returns with a 'reason'.

Example PowerShell export:

```powershell
$Env:GITHUB_PERSONAL_ACCESS_TOKEN = 'ghp_xxx'
```

Optional explicit command:

```powershell
$Env:GITHUB_MCP_COMMAND = 'docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server stdio'
```

Invoke the sample `ping` tool via your MCP client (request shape will depend on the client). Example conceptual JSON-RPC call:

```json
{
  "id": 1,
  "method": "tools/ping",
  "params": { "message": "hello" }
}
```

## Development

Run tests:

```bash
uv run pytest
```

Run lint & type checks:

```bash
uv run ruff check .
uv run mypy src
```

## Project Layout

```
src/codesage_core/
  server.py          # FastMCP app & CLI entrypoint
  tools/             # Tool modules
  schemas/           # Shared Pydantic models
```

## License

MIT
