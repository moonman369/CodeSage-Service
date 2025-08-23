# CodeSage Core

Core Model Context Protocol (MCP) server for CodeSage, implemented with **FastMCP**.

## Features

- FastMCP-based async server
- Modular tool architecture (`tools/`)
- Typed Pydantic schemas (`schemas/`)
- Example `ping` tool

## Quick Start

Install dependencies using **uv**:

```bash
uv sync
```

Run the server:

```bash
codesage-core
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
