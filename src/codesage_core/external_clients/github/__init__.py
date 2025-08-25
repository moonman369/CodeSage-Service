"""GitHub external MCP client package exports.

The previous module `github_client.py` was removed during the MCP refactor.
This package now exposes the async client + token helpers from
`github_mcp_client`. Any legacy imports of the old top-level helper functions
will raise a clear error directing developers to use `GitHubMCPAsyncClient` or
the service layer (`GitHubMCPService`).
"""

from .github_mcp_client import GitHubMCPAsyncClient, pick_token, env_token_status  # noqa: F401


def _removed(name: str):  # pragma: no cover - defensive shim
    raise RuntimeError(
        f"`{name}` helper was removed. Use `GitHubMCPAsyncClient` methods or the service layer in `services.github_mcp_service`."
    )


# Backward compatibility shims (fail fast with guidance if referenced)
def list_repositories(*args, **kwargs):  # type: ignore
    _removed('list_repositories')


def list_commits(*args, **kwargs):  # type: ignore
    _removed('list_commits')


def list_pull_requests(*args, **kwargs):  # type: ignore
    _removed('list_pull_requests')


def repository_overview(*args, **kwargs):  # type: ignore
    _removed('repository_overview')


def github_available(*args, **kwargs):  # type: ignore
    _removed('github_available')


__all__ = [
    'GitHubMCPAsyncClient',
    'pick_token',
    'env_token_status',
]
