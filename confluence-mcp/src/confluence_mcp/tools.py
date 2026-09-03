from typing import Any
from .client import ConfluenceClient


async def list_pages(c: ConfluenceClient, space_id: str | None = None, title: str | None = None, limit: int = 25) -> Any:
    if c.settings.is_cloud:
        path = f"/spaces/{space_id}/pages" if space_id else "/pages"
        return await c.get(path, params={"limit": limit, **({"title": title} if title else {})})
    params = {"type": "page", "limit": limit, "expand": "version,space", **({"spaceKey": space_id} if space_id else {}), **({"title": title} if title else {})}
    return await c.get("/content", params=params)

async def get_page(c: ConfluenceClient, page_id: str, include_body: bool = True) -> Any:
    if c.settings.is_cloud: return await c.get(f"/pages/{page_id}", params={"body-format": "storage"} if include_body else None)
    return await c.get(f"/content/{page_id}", params={"expand": "body.storage,version,space"} if include_body else None)

async def create_page(c: ConfluenceClient, space_id: str, title: str, body: str, parent_id: str | None = None) -> Any:
    if c.settings.is_cloud:
        payload = {"spaceId": space_id, "status": "current", "title": title, "body": {"representation": "storage", "value": body}}
        if parent_id: payload["parentId"] = parent_id
        return await c.post("/pages", json=payload)
    payload = {"type": "page", "title": title, "space": {"key": space_id}, "body": {"storage": {"representation": "storage", "value": body}}}
    if parent_id: payload["ancestors"] = [{"id": parent_id}]
    return await c.post("/content", json=payload)

async def update_page(c: ConfluenceClient, page_id: str, title: str, body: str, version: int, status: str = "current") -> Any:
    if c.settings.is_cloud:
        return await c.put(f"/pages/{page_id}", json={"id": page_id, "status": status, "title": title, "body": {"representation": "storage", "value": body}, "version": {"number": version}})
    return await c.put(f"/content/{page_id}", json={"id": page_id, "type": "page", "title": title, "body": {"storage": {"representation": "storage", "value": body}}, "version": {"number": version}})

async def delete_page(c: ConfluenceClient, page_id: str) -> Any: return await c.delete(f"/{'pages' if c.settings.is_cloud else 'content'}/{page_id}")
async def list_spaces(c: ConfluenceClient, limit: int = 25) -> Any: return await c.get("/spaces" if c.settings.is_cloud else "/space", params={"limit": limit})
async def get_space(c: ConfluenceClient, space_id: str) -> Any: return await c.get(f"/{'spaces' if c.settings.is_cloud else 'space'}/{space_id}")
async def list_children(c: ConfluenceClient, page_id: str, limit: int = 25) -> Any: return await c.get(f"/{'pages' if c.settings.is_cloud else 'content'}/{page_id}/{'children' if c.settings.is_cloud else 'child/page'}", params={"limit": limit})
async def list_labels(c: ConfluenceClient, page_id: str, limit: int = 25) -> Any: return await c.get(f"/{'pages' if c.settings.is_cloud else 'content'}/{page_id}/{'labels' if c.settings.is_cloud else 'label'}", params={"limit": limit})
async def list_comments(c: ConfluenceClient, page_id: str, limit: int = 25) -> Any: return await c.get(f"/{'pages' if c.settings.is_cloud else 'content'}/{page_id}/{'comments' if c.settings.is_cloud else 'child/comment'}", params={"limit": limit})
async def add_comment(c: ConfluenceClient, page_id: str, body: str) -> Any:
    if c.settings.is_cloud: return await c.post(f"/pages/{page_id}/comments", json={"body": {"representation": "storage", "value": body}})
    return await c.post("/content", json={"type": "comment", "container": {"id": page_id, "type": "page"}, "body": {"storage": {"representation": "storage", "value": body}}})
