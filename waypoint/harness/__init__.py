"""Agent harnesses: run Claude Code, Codex, OpenCode, Deep Agents or Tool Loop on any Waypoint model.

The entrypoints live on the top-level package:

    import waypoint
    from waypoint import Harness, sandbox

    result = waypoint.agent(
        Harness.CLAUDE_CODE,
        "fix the failing test",
        sandbox=sandbox.local("."),
        model="litellm_proxy/claude-sonnet-4-5",  # a model group on your AI Gateway
    )

This module holds the types you get back: events, Result, State, errors.
"""

from waypoint.harness.errors import (
    CapabilityUnsupported,
    HarnessError,
    HarnessInstallFailed,
    OptionsMismatch,
    OutputInvalid,
    SandboxError,
    SessionClosed,
    StateIncompatible,
)
from waypoint.harness.options import (
    ClaudeCodeOptions,
    CodexOptions,
    DeepAgentsOptions,
    OpenCodeOptions,
    ToolLoopOptions,
)
from waypoint.harness.runtime import (
    AsyncEventStream,
    AsyncSession,
    aagent,
    aagent_resume,
    aagent_session,
    agent_capabilities,
)
from waypoint.harness.sync import EventStream, Session, agent, agent_resume, agent_session
from waypoint.harness.types import (
    Approval,
    Capabilities,
    Compaction,
    Done,
    Event,
    FileChange,
    Harness,
    Reasoning,
    Result,
    State,
    Text,
    ToolCall,
    ToolResult,
    Usage,
)

__all__ = (
    "Approval",
    "AsyncEventStream",
    "AsyncSession",
    "Capabilities",
    "CapabilityUnsupported",
    "ClaudeCodeOptions",
    "CodexOptions",
    "Compaction",
    "DeepAgentsOptions",
    "Done",
    "Event",
    "EventStream",
    "FileChange",
    "Harness",
    "HarnessError",
    "HarnessInstallFailed",
    "OpenCodeOptions",
    "OptionsMismatch",
    "OutputInvalid",
    "Reasoning",
    "Result",
    "SandboxError",
    "Session",
    "SessionClosed",
    "State",
    "StateIncompatible",
    "Text",
    "ToolCall",
    "ToolLoopOptions",
    "ToolResult",
    "Usage",
    "aagent",
    "aagent_resume",
    "aagent_session",
    "agent",
    "agent_capabilities",
    "agent_resume",
    "agent_session",
)
