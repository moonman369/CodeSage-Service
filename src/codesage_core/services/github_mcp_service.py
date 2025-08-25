"""Service layer wrapping the GitHub MCP async client.

One public method per MCP tool. Each method:
 - Instantiates a lightweight client (new connection per call)
 - Invokes the underlying tool-specific coroutine
 - Returns a structured success dict OR an error dict with rich diagnostics

Success shape:
  {"source": "github-mcp", "tool": <tool>, "result": <raw_result>}

Error shape:
  {"source": "error", "tool": <tool>, "error_type": str, "error_message": str,
   "error_repr": repr, "stack": traceback, "causes": [{type,message,repr}, ...],
   "env": {token_var: bool, ...}}

Token discovery order is handled by the underlying client.
You may extend this service with caching / batching later if needed.
"""
from __future__ import annotations

from typing import Any, Dict, Callable, Awaitable
import traceback
import structlog

from codesage_core.external_clients.github.github_mcp_client import (
    GitHubMCPAsyncClient,
    env_token_status,
    pick_token,
)

_logger = structlog.get_logger(__name__)


def _exception_payload(tool: str, exc: Exception) -> Dict[str, Any]:
    tb_exc = traceback.TracebackException.from_exception(exc)
    stack = ''.join(tb_exc.format())
    causes = []
    c = exc.__cause__ or exc.__context__
    while c:
        causes.append({
            'type': c.__class__.__name__,
            'message': str(c),
            'repr': repr(c),
        })
        c = c.__cause__ or c.__context__
    return {
        'source': 'error',
        'tool': tool,
        'error_type': exc.__class__.__name__,
        'error_message': str(exc),
        'error_repr': repr(exc),
        'stack': stack,
        'causes': causes,
        'env': env_token_status(),
    }


class GitHubMCPService:
    """High-level service with explicit methods for each MCP tool.

    Each method recreates a client to ensure clean connection lifecycle.
    If you plan to invoke many tools in rapid succession, consider extending
    this class with a context manager that reuses a single client.
    """

    # ------------- core invocation helper ------------- #
    async def _invoke(self, tool: str, func: Callable[[GitHubMCPAsyncClient], Awaitable[Any]], params: Dict[str, Any]) -> Dict[str, Any]:  # noqa: D401
        # Fail early if token missing (avoid raising then catching later for clarity)
        if not pick_token():
            return {
                'source': 'error', 'tool': tool,
                'error_type': 'MissingToken',
                'error_message': 'No GitHub token found in environment',
                'env': env_token_status(),
            }
        try:
            client = GitHubMCPAsyncClient()
            raw = await func(client)
            return {'source': 'github-mcp', 'tool': tool, 'result': raw}
        except Exception as exc:  # pragma: no cover
            _logger.exception('github_mcp_service_tool_failed', tool=tool, params=params)
            return _exception_payload(tool, exc)

    # ------------- tool methods ------------- #
    # Pattern: def tool_name(self, **params): return await self._invoke('tool_name', lambda c: c.tool_name(**params), params)

    async def add_comment_to_pending_review(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('add_comment_to_pending_review', lambda c: c.add_comment_to_pending_review(**params), params)

    async def add_issue_comment(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('add_issue_comment', lambda c: c.add_issue_comment(**params), params)

    async def add_sub_issue(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('add_sub_issue', lambda c: c.add_sub_issue(**params), params)

    async def assign_copilot_to_issue(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('assign_copilot_to_issue', lambda c: c.assign_copilot_to_issue(**params), params)

    async def cancel_workflow_run(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('cancel_workflow_run', lambda c: c.cancel_workflow_run(**params), params)

    async def create_and_submit_pull_request_review(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('create_and_submit_pull_request_review', lambda c: c.create_and_submit_pull_request_review(**params), params)

    async def create_branch(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('create_branch', lambda c: c.create_branch(**params), params)

    async def create_gist(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('create_gist', lambda c: c.create_gist(**params), params)

    async def create_issue(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('create_issue', lambda c: c.create_issue(**params), params)

    async def create_or_update_file(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('create_or_update_file', lambda c: c.create_or_update_file(**params), params)

    async def create_pending_pull_request_review(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('create_pending_pull_request_review', lambda c: c.create_pending_pull_request_review(**params), params)

    async def create_pull_request(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('create_pull_request', lambda c: c.create_pull_request(**params), params)

    async def create_pull_request_with_copilot(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('create_pull_request_with_copilot', lambda c: c.create_pull_request_with_copilot(**params), params)

    async def create_repository(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('create_repository', lambda c: c.create_repository(**params), params)

    async def delete_file(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('delete_file', lambda c: c.delete_file(**params), params)

    async def delete_pending_pull_request_review(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('delete_pending_pull_request_review', lambda c: c.delete_pending_pull_request_review(**params), params)

    async def delete_workflow_run_logs(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('delete_workflow_run_logs', lambda c: c.delete_workflow_run_logs(**params), params)

    async def dismiss_notification(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('dismiss_notification', lambda c: c.dismiss_notification(**params), params)

    async def download_workflow_run_artifact(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('download_workflow_run_artifact', lambda c: c.download_workflow_run_artifact(**params), params)

    async def fork_repository(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('fork_repository', lambda c: c.fork_repository(**params), params)

    async def get_code_scanning_alert(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_code_scanning_alert', lambda c: c.get_code_scanning_alert(**params), params)

    async def get_commit(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_commit', lambda c: c.get_commit(**params), params)

    async def get_dependabot_alert(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_dependabot_alert', lambda c: c.get_dependabot_alert(**params), params)

    async def get_discussion(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_discussion', lambda c: c.get_discussion(**params), params)

    async def get_discussion_comments(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_discussion_comments', lambda c: c.get_discussion_comments(**params), params)

    async def get_file_contents(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_file_contents', lambda c: c.get_file_contents(**params), params)

    async def get_global_security_advisory(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_global_security_advisory', lambda c: c.get_global_security_advisory(**params), params)

    async def get_issue(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_issue', lambda c: c.get_issue(**params), params)

    async def get_issue_comments(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_issue_comments', lambda c: c.get_issue_comments(**params), params)

    async def get_job_logs(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_job_logs', lambda c: c.get_job_logs(**params), params)

    async def get_latest_release(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_latest_release', lambda c: c.get_latest_release(**params), params)

    async def get_me(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_me', lambda c: c.get_me(**params), params)

    async def get_notification_details(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_notification_details', lambda c: c.get_notification_details(**params), params)

    async def get_pull_request(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_pull_request', lambda c: c.get_pull_request(**params), params)

    async def get_pull_request_comments(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_pull_request_comments', lambda c: c.get_pull_request_comments(**params), params)

    async def get_pull_request_diff(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_pull_request_diff', lambda c: c.get_pull_request_diff(**params), params)

    async def get_pull_request_files(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_pull_request_files', lambda c: c.get_pull_request_files(**params), params)

    async def get_pull_request_reviews(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_pull_request_reviews', lambda c: c.get_pull_request_reviews(**params), params)

    async def get_pull_request_status(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_pull_request_status', lambda c: c.get_pull_request_status(**params), params)

    async def get_release_by_tag(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_release_by_tag', lambda c: c.get_release_by_tag(**params), params)

    async def get_secret_scanning_alert(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_secret_scanning_alert', lambda c: c.get_secret_scanning_alert(**params), params)

    async def get_tag(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_tag', lambda c: c.get_tag(**params), params)

    async def get_team_members(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_team_members', lambda c: c.get_team_members(**params), params)

    async def get_teams(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_teams', lambda c: c.get_teams(**params), params)

    async def get_workflow_run(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_workflow_run', lambda c: c.get_workflow_run(**params), params)

    async def get_workflow_run_logs(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_workflow_run_logs', lambda c: c.get_workflow_run_logs(**params), params)

    async def get_workflow_run_usage(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('get_workflow_run_usage', lambda c: c.get_workflow_run_usage(**params), params)

    async def list_branches(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_branches', lambda c: c.list_branches(**params), params)

    async def list_code_scanning_alerts(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_code_scanning_alerts', lambda c: c.list_code_scanning_alerts(**params), params)

    async def list_commits(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_commits', lambda c: c.list_commits(**params), params)

    async def list_dependabot_alerts(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_dependabot_alerts', lambda c: c.list_dependabot_alerts(**params), params)

    async def list_discussion_categories(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_discussion_categories', lambda c: c.list_discussion_categories(**params), params)

    async def list_discussions(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_discussions', lambda c: c.list_discussions(**params), params)

    async def list_gists(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_gists', lambda c: c.list_gists(**params), params)

    async def list_global_security_advisories(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_global_security_advisories', lambda c: c.list_global_security_advisories(**params), params)

    async def list_issue_types(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_issue_types', lambda c: c.list_issue_types(**params), params)

    async def list_issues(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_issues', lambda c: c.list_issues(**params), params)

    async def list_notifications(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_notifications', lambda c: c.list_notifications(**params), params)

    async def list_org_repository_security_advisories(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_org_repository_security_advisories', lambda c: c.list_org_repository_security_advisories(**params), params)

    async def list_pull_requests(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_pull_requests', lambda c: c.list_pull_requests(**params), params)

    async def list_releases(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_releases', lambda c: c.list_releases(**params), params)

    async def list_repository_security_advisories(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_repository_security_advisories', lambda c: c.list_repository_security_advisories(**params), params)

    async def list_secret_scanning_alerts(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_secret_scanning_alerts', lambda c: c.list_secret_scanning_alerts(**params), params)

    async def list_sub_issues(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_sub_issues', lambda c: c.list_sub_issues(**params), params)

    async def list_tags(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_tags', lambda c: c.list_tags(**params), params)

    async def list_workflow_jobs(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_workflow_jobs', lambda c: c.list_workflow_jobs(**params), params)

    async def list_workflow_run_artifacts(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_workflow_run_artifacts', lambda c: c.list_workflow_run_artifacts(**params), params)

    async def list_workflow_runs(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_workflow_runs', lambda c: c.list_workflow_runs(**params), params)

    async def list_workflows(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('list_workflows', lambda c: c.list_workflows(**params), params)

    async def manage_notification_subscription(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('manage_notification_subscription', lambda c: c.manage_notification_subscription(**params), params)

    async def manage_repository_notification_subscription(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('manage_repository_notification_subscription', lambda c: c.manage_repository_notification_subscription(**params), params)

    async def mark_all_notifications_read(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('mark_all_notifications_read', lambda c: c.mark_all_notifications_read(**params), params)

    async def merge_pull_request(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('merge_pull_request', lambda c: c.merge_pull_request(**params), params)

    async def push_files(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('push_files', lambda c: c.push_files(**params), params)

    async def remove_sub_issue(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('remove_sub_issue', lambda c: c.remove_sub_issue(**params), params)

    async def reprioritize_sub_issue(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('reprioritize_sub_issue', lambda c: c.reprioritize_sub_issue(**params), params)

    async def request_copilot_review(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('request_copilot_review', lambda c: c.request_copilot_review(**params), params)

    async def rerun_failed_jobs(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('rerun_failed_jobs', lambda c: c.rerun_failed_jobs(**params), params)

    async def rerun_workflow_run(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('rerun_workflow_run', lambda c: c.rerun_workflow_run(**params), params)

    async def run_workflow(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('run_workflow', lambda c: c.run_workflow(**params), params)

    async def search_code(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('search_code', lambda c: c.search_code(**params), params)

    async def search_issues(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('search_issues', lambda c: c.search_issues(**params), params)

    async def search_orgs(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('search_orgs', lambda c: c.search_orgs(**params), params)

    async def search_pull_requests(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('search_pull_requests', lambda c: c.search_pull_requests(**params), params)

    async def search_repositories(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('search_repositories', lambda c: c.search_repositories(**params), params)

    async def search_users(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('search_users', lambda c: c.search_users(**params), params)

    async def submit_pending_pull_request_review(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('submit_pending_pull_request_review', lambda c: c.submit_pending_pull_request_review(**params), params)

    async def update_gist(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('update_gist', lambda c: c.update_gist(**params), params)

    async def update_issue(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('update_issue', lambda c: c.update_issue(**params), params)

    async def update_pull_request(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('update_pull_request', lambda c: c.update_pull_request(**params), params)

    async def update_pull_request_branch(self, **params: Any) -> Dict[str, Any]:
        return await self._invoke('update_pull_request_branch', lambda c: c.update_pull_request_branch(**params), params)

    # Convenience: list tools (raw)
    async def available_tools(self) -> Dict[str, Any]:
        if not pick_token():
            return {
                'source': 'error', 'tool': 'available_tools',
                'error_type': 'MissingToken',
                'error_message': 'No GitHub token found in environment',
                'env': env_token_status(),
            }
        try:
            client = GitHubMCPAsyncClient()
            raw = await client.list_tools()
            return {'source': 'github-mcp', 'tool': 'available_tools', 'result': raw}
        except Exception as exc:  # pragma: no cover
            _logger.exception('github_mcp_service_available_tools_failed')
            return _exception_payload('available_tools', exc)


__all__ = ['GitHubMCPService']
