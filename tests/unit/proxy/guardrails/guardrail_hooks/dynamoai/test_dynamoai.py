"""
Test DynamoAI Guardrails integration
"""

import importlib
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import waypoint
from waypoint.caching.caching import DualCache
from waypoint.proxy._types import UserAPIKeyAuth
from waypoint.proxy.guardrails.guardrail_hooks.dynamoai import DynamoAIGuardrails
from tests._vcr_conftest_common import install_live_call_probe, record_vcr_outcome


@pytest.mark.asyncio
async def test_dynamoai_blocks_content_with_block_action():
    """
    Test that DynamoAI guardrail blocks content when finalAction is BLOCK.
    """
    # Create guardrail instance
    guardrail = DynamoAIGuardrails(
        guardrail_name="test-dynamoai",
        api_key="test-api-key",
        api_base="https://api.dynamo.ai",
    )

    # Mock the DynamoAI API response with BLOCK action
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "text": "This is harmful content",
        "textType": "MODEL_INPUT",
        "finalAction": "BLOCK",
        "appliedPolicies": [
            {
                "policy": {
                    "id": "policy-123",
                    "name": "Toxicity Policy",
                    "description": "Blocks toxic content",
                    "method": "TOXICITY",
                },
                "outputs": {
                    "action": "BLOCK",
                    "message": "Content contains toxic language",
                },
            }
        ],
    }
    mock_response.raise_for_status = MagicMock()
    with patch.object(guardrail.async_handler, "post", AsyncMock(return_value=mock_response)):
        request_data = {
            "model": "gpt-5.5",
            "messages": [{"role": "user", "content": "This is harmful content"}],
        }

        # Mock should_run_guardrail to return True
        guardrail.should_run_guardrail = MagicMock(return_value=True)

        # Test that the guardrail raises ValueError for blocked content
        with pytest.raises(ValueError, match="violation\\(s\\) detected") as exc_info:
            await guardrail.async_pre_call_hook(
                data=request_data,
                user_api_key_dict=UserAPIKeyAuth(),
                call_type="completion",
                cache=MagicMock(spec=DualCache),
            )

    # Verify the error message contains policy information
    error_message = str(exc_info.value)
    assert "Guardrail failed" in error_message
    assert "TOXICITY POLICY" in error_message.upper()
    assert "BLOCK" in error_message.upper()


@pytest.mark.asyncio
async def test_dynamoai_allows_content_with_none_action():
    """
    Test that DynamoAI guardrail allows content when finalAction is NONE.
    """
    # Create guardrail instance
    guardrail = DynamoAIGuardrails(
        guardrail_name="test-dynamoai",
        api_key="test-api-key",
        api_base="https://api.dynamo.ai",
    )

    # Mock the DynamoAI API response with NONE action (no violations)
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "text": "Hello, how are you?",
        "textType": "MODEL_INPUT",
        "finalAction": "NONE",
        "appliedPolicies": [],
    }
    mock_response.raise_for_status = MagicMock()
    with patch.object(guardrail.async_handler, "post", AsyncMock(return_value=mock_response)):
        request_data = {
            "model": "gpt-5.5",
            "messages": [{"role": "user", "content": "Hello, how are you?"}],
        }

        # Mock should_run_guardrail to return True
        guardrail.should_run_guardrail = MagicMock(return_value=True)

        # Test that the guardrail allows the content (no exception raised)
        result = await guardrail.async_pre_call_hook(
            data=request_data,
            user_api_key_dict=UserAPIKeyAuth(),
            call_type="completion",
            cache=MagicMock(spec=DualCache),
        )

    # Should return the request data unchanged
    assert result == request_data


@pytest.fixture(autouse=True)
def _vcr_outcome_gate(request, vcr):
    install_live_call_probe(request, vcr)
    yield
    record_vcr_outcome(request, vcr)


@pytest.fixture(scope="function", autouse=True)
def isolate_litellm_state():
    """
    Per-function isolation fixture.

    Saves and restores litellm callback/global state so tests don't leak
    side effects. Works safely under pytest-xdist parallel execution.
    """
    original_state = {}
    for attr in (
        "callbacks",
        "success_callback",
        "failure_callback",
        "_async_success_callback",
        "_async_failure_callback",
    ):
        if hasattr(waypoint, attr):
            val = getattr(waypoint, attr)
            original_state[attr] = val.copy() if val else []
    for attr in ("set_verbose", "cache", "num_retries"):
        if hasattr(waypoint, attr):
            original_state[attr] = getattr(waypoint, attr)
    if hasattr(waypoint, "in_memory_llm_clients_cache"):
        waypoint.in_memory_llm_clients_cache.flush_cache()
    for attr in ("success_callback", "failure_callback", "_async_success_callback", "_async_failure_callback"):
        if hasattr(waypoint, attr):
            setattr(waypoint, attr, [])
    yield
    if hasattr(waypoint, "in_memory_llm_clients_cache"):
        waypoint.in_memory_llm_clients_cache.flush_cache()
    for attr, original_value in original_state.items():
        if hasattr(waypoint, attr):
            setattr(waypoint, attr, original_value)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """
    Module-scoped setup. Reloads litellm only in single-process mode
    (skipped under xdist to avoid cross-worker interference).
    """
    import waypoint

    worker_id = os.environ.get("PYTEST_XDIST_WORKER", None)
    if worker_id is None:
        importlib.reload(waypoint)
        try:
            if hasattr(waypoint, "proxy") and hasattr(waypoint.proxy, "proxy_server"):
                import waypoint.proxy.proxy_server

                importlib.reload(waypoint.proxy.proxy_server)
        except Exception:
            pass
        if hasattr(waypoint, "in_memory_llm_clients_cache"):
            waypoint.in_memory_llm_clients_cache.flush_cache()
    yield
