from typing import Any
from .client import JiraClient

def _adf(text: str) -> dict[str, Any]:
    return {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": text}]}]}

async def search_issues(c: JiraClient, jql: str, max_results: int = 50, fields: list[str] | None = None) -> Any:
    payload = {"jql": jql, "maxResults": max_results}
    if fields: payload["fields"] = fields
    if c.settings.is_cloud: return await c.post("/search/jql", json=payload)
    return await c.get("/search", params={"jql": jql, "startAt": 0, "maxResults": max_results, **({"fields": ",".join(fields)} if fields else {})})
async def get_issue(c: JiraClient, issue_key: str, fields: list[str] | None = None) -> Any: return await c.get(f"/issue/{issue_key}", params={"fields": ",".join(fields)} if fields else None)
async def create_issue(c: JiraClient, project_key: str, issue_type: str, summary: str, description: str | None = None, extra_fields: dict[str, Any] | None = None) -> Any:
    fields: dict[str, Any] = {"project": {"key": project_key}, "issuetype": {"name": issue_type}, "summary": summary}
    if description is not None: fields["description"] = _adf(description) if c.settings.is_cloud else description
    if extra_fields: fields.update(extra_fields)
    return await c.post("/issue", json={"fields": fields})
async def update_issue(c: JiraClient, issue_key: str, fields: dict[str, Any]) -> Any: return await c.put(f"/issue/{issue_key}", json={"fields": fields})
async def delete_issue(c: JiraClient, issue_key: str) -> Any: return await c.delete(f"/issue/{issue_key}")
async def add_comment(c: JiraClient, issue_key: str, body: str) -> Any: return await c.post(f"/issue/{issue_key}/comment", json={"body": _adf(body) if c.settings.is_cloud else body})
async def list_comments(c: JiraClient, issue_key: str, limit: int = 50) -> Any: return await c.get(f"/issue/{issue_key}/comment", params={"maxResults": limit})
async def get_transitions(c: JiraClient, issue_key: str) -> Any: return await c.get(f"/issue/{issue_key}/transitions")
async def transition_issue(c: JiraClient, issue_key: str, transition_id: str, fields: dict[str, Any] | None = None) -> Any:
    payload: dict[str, Any] = {"transition": {"id": transition_id}}
    if fields: payload["fields"] = fields
    return await c.post(f"/issue/{issue_key}/transitions", json=payload)
async def assign_issue(c: JiraClient, issue_key: str, account_id: str | None = None) -> Any: return await c.put(f"/issue/{issue_key}/assignee", json={"accountId": account_id} if c.settings.is_cloud else {"name": account_id})
async def list_projects(c: JiraClient, limit: int = 50) -> Any: return await c.get("/project/search", params={"maxResults": limit})
async def get_project(c: JiraClient, project_key: str) -> Any: return await c.get(f"/project/{project_key}")
async def list_issue_types(c: JiraClient) -> Any: return await c.get("/issuetype")
