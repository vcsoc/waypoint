from typing import Final

import pytest

from waypoint._environment import environment_aliases


def test_legacy_environment_values_are_available_under_canonical_names() -> None:
    source: Final = {"LITELLM_MASTER_KEY": "legacy-key", "LITELLM_MODE": "PRODUCTION", "OTHER": "untouched"}
    aliases: Final = environment_aliases(source)
    assert dict(aliases) == {"WAYPOINT_MASTER_KEY": "legacy-key", "WAYPOINT_MODE": "PRODUCTION"}
    assert source == {"LITELLM_MASTER_KEY": "legacy-key", "LITELLM_MODE": "PRODUCTION", "OTHER": "untouched"}


@pytest.mark.parametrize("canonical", ("new-key", ""))
def test_canonical_environment_values_win_even_when_explicitly_empty(canonical: str) -> None:
    source: Final = {"LITELLM_MASTER_KEY": "legacy-key", "WAYPOINT_MASTER_KEY": canonical}
    assert not environment_aliases(source)
    assert source["WAYPOINT_MASTER_KEY"] == canonical
