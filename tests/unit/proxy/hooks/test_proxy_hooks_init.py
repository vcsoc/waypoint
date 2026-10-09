"""Regression guard for the enterprise hook registration / import cycle.

Python 3.13 is stricter about partially-initialized modules and surfaces
cycles that Python 3.12 silently tolerated. The previous bug:

  waypoint.proxy.hooks.__init__
    -> enterprise.enterprise_hooks
    -> waypoint_enterprise.proxy.hooks.managed_files
    -> waypoint.llms.base_llm.managed_resources.isolation
    -> waypoint.proxy.management_endpoints.common_utils
    -> waypoint.proxy.utils  (re-enters waypoint.proxy.hooks mid-init)

silently swallowed the ImportError in `hooks/__init__.py`, leaving
``managed_files`` unregistered and the /files endpoint returning 500.
"""

import pytest

from waypoint.proxy.hooks import PROXY_HOOKS, get_proxy_hook


def test_managed_files_hook_registered():
    pytest.importorskip("litellm_enterprise")
    assert "managed_files" in PROXY_HOOKS
    hook_cls = get_proxy_hook("managed_files")
    assert hook_cls.__name__ == "_PROXY_LiteLLMManagedFiles"


def test_managed_vector_stores_hook_registered():
    pytest.importorskip("litellm_enterprise")
    assert "managed_vector_stores" in PROXY_HOOKS
    hook_cls = get_proxy_hook("managed_vector_stores")
    assert hook_cls.__name__ == "_PROXY_LiteLLMManagedVectorStores"


def test_isolation_module_does_not_pull_in_proxy_utils():
    """Layering guard: waypoint.llms.* must not transitively import
    waypoint.proxy.utils, which would reintroduce the import cycle."""
    import importlib
    import sys

    for mod in [
        "waypoint.proxy.utils",
        "waypoint.proxy.management_endpoints.common_utils",
        "waypoint.llms.base_llm.managed_resources.isolation",
    ]:
        sys.modules.pop(mod, None)

    importlib.import_module("waypoint.llms.base_llm.managed_resources.isolation")
    assert "waypoint.proxy.utils" not in sys.modules
    assert "waypoint.proxy.management_endpoints.common_utils" not in sys.modules
