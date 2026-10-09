from collections.abc import Mapping
from types import MappingProxyType


def environment_aliases(environ: Mapping[str, str]) -> Mapping[str, str]:
    return MappingProxyType(
        {
            f"WAYPOINT_{key.removeprefix('LITELLM_')}": value
            for key, value in environ.items()
            if key.startswith("LITELLM_") and f"WAYPOINT_{key.removeprefix('LITELLM_')}" not in environ
        }
    )
