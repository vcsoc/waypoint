import asyncio
import importlib
import os

import pytest

import waypoint
from waypoint.waypoint_core_utils.logging_worker import GLOBAL_LOGGING_WORKER
from waypoint.types.files import (
    FILE_EXTENSIONS,
    FILE_MIME_TYPES,
    FileType,
    get_file_extension_for_file_type,
    get_file_extension_from_mime_type,
    get_file_mime_type_for_file_type,
    get_file_mime_type_from_extension,
    get_file_type_from_extension,
)
from waypoint.utils import _invalidate_model_cost_lowercase_map
from tests._vcr_conftest_common import install_live_call_probe, record_vcr_outcome


class TestFileConsts:
    def test_all_file_types_have_extensions(self):
        for file_type in FileType:
            assert file_type in FILE_EXTENSIONS.keys()

    def test_all_file_types_have_mime_types(self):
        for file_type in FileType:
            assert file_type in FILE_MIME_TYPES.keys()

    def test_get_file_extension_from_mime_type(self):
        assert get_file_extension_from_mime_type("audio/aac") == "aac"
        assert get_file_extension_from_mime_type("application/pdf") == "pdf"
        with pytest.raises(ValueError, match="Unknown extension for mime type: application"):
            get_file_extension_from_mime_type("application/unknown")

    def test_get_file_type_from_extension(self):
        assert get_file_type_from_extension("aac") == FileType.AAC
        assert get_file_type_from_extension("pdf") == FileType.PDF
        with pytest.raises(ValueError, match="Unknown file type for extension: unknown"):
            get_file_type_from_extension("unknown")

    def test_get_file_extension_for_file_type(self):
        assert get_file_extension_for_file_type(FileType.AAC) == "aac"
        assert get_file_extension_for_file_type(FileType.PDF) == "pdf"

    def test_get_file_mime_type_for_file_type(self):
        assert get_file_mime_type_for_file_type(FileType.AAC) == "audio/aac"
        assert get_file_mime_type_for_file_type(FileType.PDF) == "application/pdf"

    def test_get_file_mime_type_from_extension(self):
        assert get_file_mime_type_from_extension("aac") == "audio/aac"
        assert get_file_mime_type_from_extension("pdf") == "application/pdf"

    def test_uppercase_extensions(self):
        # Test that uppercase extensions return the correct file type
        assert get_file_type_from_extension("AAC") == FileType.AAC
        assert get_file_type_from_extension("PDF") == FileType.PDF

        # Test that uppercase extensions return the correct MIME type
        assert get_file_mime_type_from_extension("AAC") == "audio/aac"
        assert get_file_mime_type_from_extension("PDF") == "application/pdf"


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
