import waypoint
from waypoint.waypoint_core_utils.logging_callback_manager import LoggingCallbackManager
from waypoint.integrations.langfuse.langfuse_prompt_management import (
    LangfusePromptManagement,
)
from waypoint.integrations.opentelemetry import OpenTelemetry
def test_duplicate_langfuse_logger_test():
    manager = LoggingCallbackManager()
    for _ in range(10):
        langfuse_logger = LangfusePromptManagement()
        manager.add_litellm_success_callback(langfuse_logger)
    print("waypoint.success_callback: ", waypoint.success_callback)
    assert len(waypoint.success_callback) == 1


def test_duplicate_multiple_loggers_test():
    manager = LoggingCallbackManager()
    for _ in range(10):
        langfuse_logger = LangfusePromptManagement()
        otel_logger = OpenTelemetry()
        manager.add_litellm_success_callback(langfuse_logger)
        manager.add_litellm_success_callback(otel_logger)
    print("waypoint.success_callback: ", waypoint.success_callback)
    assert len(waypoint.success_callback) == 2

    # Check exactly one instance of each logger type
    langfuse_count = sum(
        1
        for callback in waypoint.success_callback
        if isinstance(callback, LangfusePromptManagement)
    )
    otel_count = sum(
        1
        for callback in waypoint.success_callback
        if isinstance(callback, OpenTelemetry)
    )

    assert (
        langfuse_count == 1
    ), "Should have exactly one LangfusePromptManagement instance"
    assert otel_count == 1, "Should have exactly one OpenTelemetry instance"
