"""
Waypoint Skills Hook - Proxy integration for skills

This module provides the CustomLogger hook for skills processing.
The actual skill logic is in waypoint/llms/waypoint_proxy/skills/.

Usage:
    from waypoint.proxy.hooks.waypoint_skills import SkillsInjectionHook

    # Register hook in proxy
    waypoint.callbacks.append(SkillsInjectionHook())
"""

# Re-export from the SDK location for convenience
from waypoint.llms.waypoint_proxy.skills import (
    LITELLM_CODE_EXECUTION_TOOL,
    CodeExecutionHandler,
    LiteLLMInternalTools,
    SkillPromptInjectionHandler,
    SkillsSandboxExecutor,
    code_execution_handler,
    get_litellm_code_execution_tool,
)
from waypoint.proxy.hooks.waypoint_skills.main import SkillsInjectionHook

__all__ = [
    "LITELLM_CODE_EXECUTION_TOOL",
    "CodeExecutionHandler",
    "LiteLLMInternalTools",
    "SkillPromptInjectionHandler",
    "SkillsInjectionHook",
    "SkillsSandboxExecutor",
    "code_execution_handler",
    "get_litellm_code_execution_tool",
]
