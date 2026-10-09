import pickle
from importlib import import_module
from typing import Final

from pydantic import TypeAdapter

from waypoint.cost_calculator import completion_cost
from waypoint.proxy._experimental.mcp_server.auth.waypoint_auth_handler import MCPAuthenticatedUser
from waypoint.proxy._types import UserAPIKeyAuth
from waypoint.types.utils import ModelResponse


def test_legacy_serialized_response_can_be_costed_by_waypoint() -> None:
    legacy_type: Final = TypeAdapter(type[ModelResponse]).validate_python(
        pickle.loads(b"clitellm.types.utils\nModelResponse\n.")
    )
    response: Final = legacy_type(model="compat-model", usage={"prompt_tokens": 3, "completion_tokens": 2})
    assert completion_cost(
        completion_response=response,
        custom_cost_per_token={"input_cost_per_token": 0.5, "output_cost_per_token": 1.0},
    ) == 3 * 0.5 + 2 * 1.0


def test_legacy_and_canonical_imports_share_runtime_configuration() -> None:
    legacy: Final = import_module("litellm.waypoint_core_utils.waypoint_logging")
    canonical: Final = import_module("waypoint.waypoint_core_utils.waypoint_logging")
    historical: Final = import_module("litellm.litellm_core_utils.litellm_logging")
    assert legacy is canonical
    assert historical is canonical


def test_legacy_mcp_authentication_retains_identity_and_forwarded_headers() -> None:
    legacy_type: Final = TypeAdapter(type[MCPAuthenticatedUser]).validate_python(
        import_module("litellm.proxy._experimental.mcp_server.auth.litellm_auth_handler").MCPAuthenticatedUser
    )
    identity: Final = UserAPIKeyAuth(user_id="compat-user", team_id="compat-team")
    context: Final = legacy_type(user_api_key_auth=identity, raw_headers={"x-request-id": "compat-request"})
    assert context.user_api_key_auth is identity
    assert context.raw_headers == {"x-request-id": "compat-request"}
