import asyncio
import importlib
import os
import warnings

import pytest

import waypoint
from waypoint.waypoint_core_utils.logging_worker import GLOBAL_LOGGING_WORKER
from waypoint.utils import _invalidate_model_cost_lowercase_map
from tests._vcr_conftest_common import install_live_call_probe, record_vcr_outcome


def test_namespace_conflict_warning():
    with warnings.catch_warnings(record=True) as recorded_warnings:
        warnings.simplefilter("always")  # Capture all warnings
        import waypoint

    # Check that no warning with the specific message was raised
    assert not any("conflict with protected namespace" in str(w.message) for w in recorded_warnings), (
        "Test failed: 'conflict with protected namespace' warning was encountered!"
    )


@pytest.fixture(autouse=True)
def _vcr_outcome_gate(request, vcr):
    install_live_call_probe(request, vcr)
    yield
    record_vcr_outcome(request, vcr)


@pytest.fixture(scope="function", autouse=True)
def isolate_litellm_state():
    """
    Per-function isolation fixture.

    Resets litellm globals to their true defaults before each test and
    restores them afterward, so tests don't leak side effects.
    Works safely under pytest-xdist parallel execution.
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
    for attr in ("pre_call_rules", "post_call_rules"):
        if hasattr(waypoint, attr):
            val = getattr(waypoint, attr)
            original_state[attr] = val.copy() if val else []
    for attr in _SCALAR_DEFAULTS:
        if hasattr(waypoint, attr):
            original_state[attr] = getattr(waypoint, attr)
    if hasattr(waypoint, "in_memory_llm_clients_cache"):
        waypoint.in_memory_llm_clients_cache.flush_cache()
    for attr in (
        "callbacks",
        "success_callback",
        "failure_callback",
        "_async_success_callback",
        "_async_failure_callback",
        "pre_call_rules",
        "post_call_rules",
    ):
        if hasattr(waypoint, attr):
            setattr(waypoint, attr, [])
    for attr, default_val in _SCALAR_DEFAULTS.items():
        if hasattr(waypoint, attr):
            setattr(waypoint, attr, default_val)
    yield
    asyncio.run(GLOBAL_LOGGING_WORKER.clear_queue())
    if hasattr(waypoint, "in_memory_llm_clients_cache"):
        waypoint.in_memory_llm_clients_cache.flush_cache()
    for attr, original_value in original_state.items():
        if hasattr(waypoint, attr):
            setattr(waypoint, attr, original_value)
    _invalidate_model_cost_lowercase_map()


_SCALAR_DEFAULTS = {
    "num_retries": getattr(waypoint, "num_retries", None),
    "num_retries_per_request": getattr(waypoint, "num_retries_per_request", None),
    "request_timeout": getattr(waypoint, "request_timeout", None),
    "set_verbose": getattr(waypoint, "set_verbose", False),
    "cache": getattr(waypoint, "cache", None),
    "allowed_fails": getattr(waypoint, "allowed_fails", 3),
    "default_fallbacks": getattr(waypoint, "default_fallbacks", None),
    "enable_azure_ad_token_refresh": getattr(waypoint, "enable_azure_ad_token_refresh", None),
    "tag_budget_config": getattr(waypoint, "tag_budget_config", None),
    "model_cost": getattr(waypoint, "model_cost", None),
    "token_counter": getattr(waypoint, "token_counter", None),
    "disable_aiohttp_transport": getattr(waypoint, "disable_aiohttp_transport", False),
    "force_ipv4": getattr(waypoint, "force_ipv4", False),
    "drop_params": getattr(waypoint, "drop_params", None),
    "modify_params": getattr(waypoint, "modify_params", False),
    "api_base": getattr(waypoint, "api_base", None),
    "api_key": getattr(waypoint, "api_key", None),
}


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
