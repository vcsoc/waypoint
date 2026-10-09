"""
Test Azure AI Kimi K2.6 model metadata.
"""

import json
from importlib.resources import files

import pytest


@pytest.fixture(scope="module")
def use_local_model_cost_map():
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv("WAYPOINT_LOCAL_MODEL_COST_MAP", "True")

    import waypoint
    from waypoint.utils import _invalidate_model_cost_lowercase_map

    original_model_cost = waypoint.model_cost
    waypoint.model_cost = json.loads(
        files("waypoint")
        .joinpath("model_prices_and_context_window_backup.json")
        .read_text(encoding="utf-8")
    )
    waypoint.get_model_info.cache_clear()
    _invalidate_model_cost_lowercase_map()
    try:
        yield waypoint
    finally:
        waypoint.model_cost = original_model_cost
        waypoint.get_model_info.cache_clear()
        _invalidate_model_cost_lowercase_map()
        monkeypatch.undo()


