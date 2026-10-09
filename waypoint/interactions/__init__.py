"""
Waypoint Interactions API

This module provides SDK methods for Google's Interactions API.

Usage:
    import waypoint

    # Create an interaction with a model
    response = waypoint.interactions.create(
        model="gemini-2.5-flash",
        input="Hello, how are you?"
    )

    # Create an interaction with an agent
    response = waypoint.interactions.create(
        agent="deep-research-pro-preview-12-2025",
        input="Research the current state of cancer research"
    )

    # Async version
    response = await waypoint.interactions.acreate(...)

    # Get an interaction
    response = waypoint.interactions.get(interaction_id="...")

    # Delete an interaction
    result = waypoint.interactions.delete(interaction_id="...")

    # Cancel an interaction
    result = waypoint.interactions.cancel(interaction_id="...")

    # Create a managed agent on the provider side
    result = waypoint.interactions.agents.create(
        name="waverunner",
        custom_llm_provider="gemini",
        api_key="...",
        base_agent="gemini-2.5-flash",
        instructions="You are a helpful assistant.",
    )

Methods:
- create(): Sync create interaction
- acreate(): Async create interaction
- get(): Sync get interaction
- aget(): Async get interaction
- delete(): Sync delete interaction
- adelete(): Async delete interaction
- cancel(): Sync cancel interaction
- acancel(): Async cancel interaction

Sub-modules:
- agents: Provider-side agent creation (waypoint.interactions.agents.create)
"""

from waypoint.interactions import agents
from waypoint.interactions.main import (
    acancel,
    acreate,
    adelete,
    aget,
    cancel,
    create,
    delete,
    get,
)

__all__ = [
    "acancel",
    "acreate",
    "adelete",
    "agents",
    "aget",
    "cancel",
    "create",
    "delete",
    "get",
]
