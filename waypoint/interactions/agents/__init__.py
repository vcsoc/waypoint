"""
waypoint.interactions.agents

Full CRUD SDK for provider-side managed agents (e.g. Gemini v1beta/agents).

    waypoint.interactions.agents.create(name=..., ...)
    waypoint.interactions.agents.list(api_key=...)
    waypoint.interactions.agents.get(name=..., ...)
    waypoint.interactions.agents.delete(name=..., ...)
    waypoint.interactions.agents.list_versions(name=..., ...)

Async counterparts: acreate, alist, aget, adelete, alist_versions
"""

from waypoint.interactions.agents.main import (
    acreate,
    adelete,
    aget,
    alist,
    alist_versions,
    create,
    delete,
    get,
    list,
    list_versions,
)

__all__ = [
    "acreate",
    "adelete",
    "aget",
    "alist",
    "alist_versions",
    "create",
    "delete",
    "get",
    "list",
    "list_versions",
]
