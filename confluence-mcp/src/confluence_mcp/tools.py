from typing import Any
from .client import ConfluenceClient


async def list_pages(c: ConfluenceClient, space_id: str | None = None, title: str | None = None, limit: int = 25) -> Any:
    path = f"/spaces/{space_id}/pages" if space_id else "/pages"
    return await c.get(path, params={"limit": limit, **({"title": title} if title else {})})

async def get_page(c: ConfluenceClient, page_id: str, include_body: bool = True) -> Any:
    return await c.get(f"/pages/{page_id}", params={"body-format": "storage"} if include_body else None)

async def create_page(c: ConfluenceClient, space_id: str, title: str, body: str, parent_id: str | None = None) -> Any:
    payload = {"spaceId": space_id, "status": "current", "title": title,
               "body": {"representation": "storage", "value": body}}
    if parent_id: payload["parentId"] = parent_id
    return await c.post("/pages", json=payload)

async def update_page(c: ConfluenceClient, page_id: str, title: str, body: str, version: int, status: str = "current") -> Any:
    return await c.put(f"/pages/{page_id}", json={"id": page_id, "status": status, "title": title,
        "body": {"representation": "storage", "value": body}, "version": {"number": version}})

async def delete_page(c: ConfluenceClient, page_id: str) -> Any: return await c.delete(f"/pages/{page_id}")
async def list_spaces(c: ConfluenceClient, limit: int = 25) -> Any: return await c.get("/spaces", params={"limit": limit})
async def get_space(c: ConfluenceClient, space_id: str) -> Any: return await c.get(f"/spaces/{space_id}")
async def list_children(c: ConfluenceClient, page_id: str, limit: int = 25) -> Any: return await c.get(f"/pages/{page_id}/children", params={"limit": limit})
async def list_labels(c: ConfluenceClient, page_id: str, limit: int = 25) -> Any: return await c.get(f"/pages/{page_id}/labels", params={"limit": limit})
async def list_comments(c: ConfluenceClient, page_id: str, limit: int = 25) -> Any: return await c.get(f"/pages/{page_id}/comments", params={"limit": limit})
async def add_comment(c: ConfluenceClient, page_id: str, body: str) -> Any:
    return await c.post(f"/pages/{page_id}/comments", json={"body": {"representation": "storage", "value": body}})
