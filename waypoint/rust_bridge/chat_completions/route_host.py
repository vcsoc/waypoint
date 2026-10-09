from __future__ import annotations

from collections.abc import Mapping
from typing import Final

import waypoint
from waypoint.constants import OPENAI_CHAT_COMPLETION_PARAMS
from waypoint.rust_bridge import failures
from waypoint.rust_bridge.public_call import optional_str
from waypoint.types.utils import ModelResponse

_TRANSPORT_PARAMETERS: Final = frozenset(
    {
        "api_base",
        "api_key",
        "api_version",
        "deployment_id",
        "organization",
        "base_url",
        "default_headers",
        "timeout",
        "request_timeout",
        "max_retries",
        "extra_headers",
    }
)
PARAMETERS: Final = tuple(name for name in OPENAI_CHAT_COMPLETION_PARAMS if name not in _TRANSPORT_PARAMETERS)


def connection_defaults(provider: str) -> tuple[str | None, str | None]:
    if provider == "anthropic":
        return waypoint.anthropic_key or waypoint.api_key, waypoint.api_base
    return None, None


def response(value: Mapping[str, object]) -> ModelResponse:
    return ModelResponse(**value)


def map_failure(error: Exception, request: Mapping[str, object]) -> Exception:
    provider: Final = optional_str(request.get("custom_llm_provider")) or str(request["model"]).partition("/")[0]
    return failures.map_native_failure(
        error,
        str(request["model"]),
        provider,
        request,
        optional_str(request.get("api_base")) or optional_str(request.get("base_url")),
    )
