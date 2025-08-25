"""Auto-generated GitHub MCP client wrappers.

This module provides a single async client class plus one convenience coroutine
per tool exposed by the GitHub MCP server (based on `github_mcp_tool_list.json`).

Usage example:
	from codesage_core.external_clients.github.github_mcp_client import GitHubMCPAsyncClient

	client = GitHubMCPAsyncClient()  # token auto-picked from env
	repos = await client.search_repositories(query="language:python topic:mcp")

Token discovery order:
  GITHUB_PERSONAL_ACCESS_TOKEN > GITHUB_TOKEN > GITHUB_PAT

All wrapper methods accept **params and forward them directly to the remote
tool. Input schemas in the current exported list are generic (type: object), so
we do not enforce parameter validation here.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, Callable, Awaitable
import os

# Optional .env loading so tokens can be supplied via a local development file.
# Executes once at import; failures are silent to avoid hard dependency.
try:  # pragma: no cover - best-effort convenience
	from dotenv import load_dotenv  # type: ignore
except Exception:  # pragma: no cover
	load_dotenv = None  # type: ignore

if load_dotenv:  # Only attempt if python-dotenv is installed
	try:
		load_dotenv()  # do not override existing environment
	except Exception:  # pragma: no cover
		pass

try:  # Support both hypothetical capitalized & actual package name
	from FastMCP import Client as MCPClient  # type: ignore
except ImportError:  # pragma: no cover
	from fastmcp import Client as MCPClient  # type: ignore

DEFAULT_SERVER_URL = "https://api.githubcopilot.com/mcp/"
TOKEN_ENV_ORDER = [
	"GITHUB_PERSONAL_ACCESS_TOKEN",
	"GITHUB_TOKEN",
	"GITHUB_PAT",
]


def pick_token() -> Optional[str]:
	for k in TOKEN_ENV_ORDER:
		v = os.getenv(k)
		if v:
			return v
	return None


def env_token_status() -> Dict[str, bool]:
	return {k: bool(os.getenv(k)) for k in TOKEN_ENV_ORDER}


class GitHubMCPAsyncClient:
	"""Async wrapper around the MCP client with per-tool helper methods."""

	def __init__(
		self,
		token: Optional[str] = None,
		server_url: Optional[str] = None,
	) -> None:
		self.server_url = server_url or os.getenv("GITHUB_MCP_URL", DEFAULT_SERVER_URL)
		self.token = token or pick_token()
		if not self.token:
			raise RuntimeError(
				"Missing GitHub token (set one of GITHUB_PERSONAL_ACCESS_TOKEN, GITHUB_TOKEN, GITHUB_PAT)"
			)

	# ---------------- core low-level call helpers ---------------- #
	async def call(self, tool: str, params: Dict[str, Any] | None = None) -> Any:
		params = params or {}
		async with MCPClient(self.server_url, auth=self.token) as client:
			return await client.call_tool(tool, params)

	async def list_tools(self) -> Any:
		async with MCPClient(self.server_url, auth=self.token) as client:
			return await client.list_tools()

	# ---------------- generated tool wrapper methods ---------------- #
	# Each of these simply forwards **params to the underlying MCP tool.

	async def add_comment_to_pending_review(self, **params: Any) -> Any:  # Add review comment to latest pending PR review
		return await self.call("add_comment_to_pending_review", params)

	async def add_issue_comment(self, **params: Any) -> Any:  # Add a comment to an issue
		return await self.call("add_issue_comment", params)

	async def add_sub_issue(self, **params: Any) -> Any:  # Add a sub-issue to a parent issue
		return await self.call("add_sub_issue", params)

	async def assign_copilot_to_issue(self, **params: Any) -> Any:  # Assign Copilot to an issue
		return await self.call("assign_copilot_to_issue", params)

	async def cancel_workflow_run(self, **params: Any) -> Any:  # Cancel a workflow run
		return await self.call("cancel_workflow_run", params)

	async def create_and_submit_pull_request_review(self, **params: Any) -> Any:  # Create+submit PR review (no comments)
		return await self.call("create_and_submit_pull_request_review", params)

	async def create_branch(self, **params: Any) -> Any:  # Create branch
		return await self.call("create_branch", params)

	async def create_gist(self, **params: Any) -> Any:  # Create gist
		return await self.call("create_gist", params)

	async def create_issue(self, **params: Any) -> Any:  # Create issue
		return await self.call("create_issue", params)

	async def create_or_update_file(self, **params: Any) -> Any:  # Create or update single file
		return await self.call("create_or_update_file", params)

	async def create_pending_pull_request_review(self, **params: Any) -> Any:  # Create pending PR review
		return await self.call("create_pending_pull_request_review", params)

	async def create_pull_request(self, **params: Any) -> Any:  # Create pull request
		return await self.call("create_pull_request", params)

	async def create_pull_request_with_copilot(self, **params: Any) -> Any:  # Delegate task to Copilot agent
		return await self.call("create_pull_request_with_copilot", params)

	async def create_repository(self, **params: Any) -> Any:  # Create repository
		return await self.call("create_repository", params)

	async def delete_file(self, **params: Any) -> Any:  # Delete file
		return await self.call("delete_file", params)

	async def delete_pending_pull_request_review(self, **params: Any) -> Any:  # Delete pending PR review
		return await self.call("delete_pending_pull_request_review", params)

	async def delete_workflow_run_logs(self, **params: Any) -> Any:  # Delete workflow run logs
		return await self.call("delete_workflow_run_logs", params)

	async def dismiss_notification(self, **params: Any) -> Any:  # Dismiss notification
		return await self.call("dismiss_notification", params)

	async def download_workflow_run_artifact(self, **params: Any) -> Any:  # Get artifact download URL
		return await self.call("download_workflow_run_artifact", params)

	async def fork_repository(self, **params: Any) -> Any:  # Fork repository
		return await self.call("fork_repository", params)

	async def get_code_scanning_alert(self, **params: Any) -> Any:  # Get code scanning alert details
		return await self.call("get_code_scanning_alert", params)

	async def get_commit(self, **params: Any) -> Any:  # Get commit details
		return await self.call("get_commit", params)

	async def get_dependabot_alert(self, **params: Any) -> Any:  # Get Dependabot alert details
		return await self.call("get_dependabot_alert", params)

	async def get_discussion(self, **params: Any) -> Any:  # Get discussion by ID
		return await self.call("get_discussion", params)

	async def get_discussion_comments(self, **params: Any) -> Any:  # Get discussion comments
		return await self.call("get_discussion_comments", params)

	async def get_file_contents(self, **params: Any) -> Any:  # Get file or directory contents
		return await self.call("get_file_contents", params)

	async def get_global_security_advisory(self, **params: Any) -> Any:  # Get global security advisory
		return await self.call("get_global_security_advisory", params)

	async def get_issue(self, **params: Any) -> Any:  # Get issue details
		return await self.call("get_issue", params)

	async def get_issue_comments(self, **params: Any) -> Any:  # Get issue comments
		return await self.call("get_issue_comments", params)

	async def get_job_logs(self, **params: Any) -> Any:  # Download job logs / failed logs
		return await self.call("get_job_logs", params)

	async def get_latest_release(self, **params: Any) -> Any:  # Get latest release
		return await self.call("get_latest_release", params)

	async def get_me(self, **params: Any) -> Any:  # Authenticated user profile
		return await self.call("get_me", params)

	async def get_notification_details(self, **params: Any) -> Any:  # Notification details
		return await self.call("get_notification_details", params)

	async def get_pull_request(self, **params: Any) -> Any:  # Pull request details
		return await self.call("get_pull_request", params)

	async def get_pull_request_comments(self, **params: Any) -> Any:  # PR comments
		return await self.call("get_pull_request_comments", params)

	async def get_pull_request_diff(self, **params: Any) -> Any:  # PR diff
		return await self.call("get_pull_request_diff", params)

	async def get_pull_request_files(self, **params: Any) -> Any:  # Files changed in PR
		return await self.call("get_pull_request_files", params)

	async def get_pull_request_reviews(self, **params: Any) -> Any:  # PR reviews
		return await self.call("get_pull_request_reviews", params)

	async def get_pull_request_status(self, **params: Any) -> Any:  # PR status
		return await self.call("get_pull_request_status", params)

	async def get_release_by_tag(self, **params: Any) -> Any:  # Release by tag
		return await self.call("get_release_by_tag", params)

	async def get_secret_scanning_alert(self, **params: Any) -> Any:  # Secret scanning alert
		return await self.call("get_secret_scanning_alert", params)

	async def get_tag(self, **params: Any) -> Any:  # Git tag details
		return await self.call("get_tag", params)

	async def get_team_members(self, **params: Any) -> Any:  # Team members
		return await self.call("get_team_members", params)

	async def get_teams(self, **params: Any) -> Any:  # Teams for user/org
		return await self.call("get_teams", params)

	async def get_workflow_run(self, **params: Any) -> Any:  # Workflow run details
		return await self.call("get_workflow_run", params)

	async def get_workflow_run_logs(self, **params: Any) -> Any:  # Workflow run logs ZIP
		return await self.call("get_workflow_run_logs", params)

	async def get_workflow_run_usage(self, **params: Any) -> Any:  # Workflow run usage metrics
		return await self.call("get_workflow_run_usage", params)

	async def list_branches(self, **params: Any) -> Any:  # List branches
		return await self.call("list_branches", params)

	async def list_code_scanning_alerts(self, **params: Any) -> Any:  # List code scanning alerts
		return await self.call("list_code_scanning_alerts", params)

	async def list_commits(self, **params: Any) -> Any:  # List commits for branch/ref
		return await self.call("list_commits", params)

	async def list_dependabot_alerts(self, **params: Any) -> Any:  # List dependabot alerts
		return await self.call("list_dependabot_alerts", params)

	async def list_discussion_categories(self, **params: Any) -> Any:  # Discussion categories
		return await self.call("list_discussion_categories", params)

	async def list_discussions(self, **params: Any) -> Any:  # Discussions
		return await self.call("list_discussions", params)

	async def list_gists(self, **params: Any) -> Any:  # User gists
		return await self.call("list_gists", params)

	async def list_global_security_advisories(self, **params: Any) -> Any:  # Global advisories
		return await self.call("list_global_security_advisories", params)

	async def list_issue_types(self, **params: Any) -> Any:  # Supported issue types
		return await self.call("list_issue_types", params)

	async def list_issues(self, **params: Any) -> Any:  # Repository issues
		return await self.call("list_issues", params)

	async def list_notifications(self, **params: Any) -> Any:  # Notifications for user
		return await self.call("list_notifications", params)

	async def list_org_repository_security_advisories(self, **params: Any) -> Any:  # Org repo advisories
		return await self.call("list_org_repository_security_advisories", params)

	async def list_pull_requests(self, **params: Any) -> Any:  # Pull requests
		return await self.call("list_pull_requests", params)

	async def list_releases(self, **params: Any) -> Any:  # Releases
		return await self.call("list_releases", params)

	async def list_repository_security_advisories(self, **params: Any) -> Any:  # Repo advisories
		return await self.call("list_repository_security_advisories", params)

	async def list_secret_scanning_alerts(self, **params: Any) -> Any:  # Secret scanning alerts
		return await self.call("list_secret_scanning_alerts", params)

	async def list_sub_issues(self, **params: Any) -> Any:  # Sub-issues of issue
		return await self.call("list_sub_issues", params)

	async def list_tags(self, **params: Any) -> Any:  # Git tags
		return await self.call("list_tags", params)

	async def list_workflow_jobs(self, **params: Any) -> Any:  # Jobs for workflow run
		return await self.call("list_workflow_jobs", params)

	async def list_workflow_run_artifacts(self, **params: Any) -> Any:  # Artifacts for workflow run
		return await self.call("list_workflow_run_artifacts", params)

	async def list_workflow_runs(self, **params: Any) -> Any:  # Workflow runs
		return await self.call("list_workflow_runs", params)

	async def list_workflows(self, **params: Any) -> Any:  # Workflows in repo
		return await self.call("list_workflows", params)

	async def manage_notification_subscription(self, **params: Any) -> Any:  # Manage notification subscription
		return await self.call("manage_notification_subscription", params)

	async def manage_repository_notification_subscription(self, **params: Any) -> Any:  # Manage repo notification subscription
		return await self.call("manage_repository_notification_subscription", params)

	async def mark_all_notifications_read(self, **params: Any) -> Any:  # Mark notifications read
		return await self.call("mark_all_notifications_read", params)

	async def merge_pull_request(self, **params: Any) -> Any:  # Merge pull request
		return await self.call("merge_pull_request", params)

	async def push_files(self, **params: Any) -> Any:  # Push multiple files (single commit)
		return await self.call("push_files", params)

	async def remove_sub_issue(self, **params: Any) -> Any:  # Remove sub-issue link
		return await self.call("remove_sub_issue", params)

	async def reprioritize_sub_issue(self, **params: Any) -> Any:  # Reprioritize sub-issue
		return await self.call("reprioritize_sub_issue", params)

	async def request_copilot_review(self, **params: Any) -> Any:  # Request Copilot PR review
		return await self.call("request_copilot_review", params)

	async def rerun_failed_jobs(self, **params: Any) -> Any:  # Rerun failed jobs
		return await self.call("rerun_failed_jobs", params)

	async def rerun_workflow_run(self, **params: Any) -> Any:  # Rerun entire workflow run
		return await self.call("rerun_workflow_run", params)

	async def run_workflow(self, **params: Any) -> Any:  # Dispatch a workflow
		return await self.call("run_workflow", params)

	async def search_code(self, **params: Any) -> Any:  # Search code
		return await self.call("search_code", params)

	async def search_issues(self, **params: Any) -> Any:  # Search issues
		return await self.call("search_issues", params)

	async def search_orgs(self, **params: Any) -> Any:  # Search organizations
		return await self.call("search_orgs", params)

	async def search_pull_requests(self, **params: Any) -> Any:  # Search pull requests
		return await self.call("search_pull_requests", params)

	async def search_repositories(self, **params: Any) -> Any:  # Search repositories
		return await self.call("search_repositories", params)

	async def search_users(self, **params: Any) -> Any:  # Search users
		return await self.call("search_users", params)

	async def submit_pending_pull_request_review(self, **params: Any) -> Any:  # Submit pending PR review
		return await self.call("submit_pending_pull_request_review", params)

	async def update_gist(self, **params: Any) -> Any:  # Update gist
		return await self.call("update_gist", params)

	async def update_issue(self, **params: Any) -> Any:  # Update issue
		return await self.call("update_issue", params)

	async def update_pull_request(self, **params: Any) -> Any:  # Update pull request
		return await self.call("update_pull_request", params)

	async def update_pull_request_branch(self, **params: Any) -> Any:  # Update PR branch
		return await self.call("update_pull_request_branch", params)


__all__ = ["GitHubMCPAsyncClient", "pick_token", "env_token_status"]

