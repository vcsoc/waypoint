"""
Type definitions for the Waypoint Policy Engine.

This module re-exports types from waypoint.types.proxy.policy_engine for backward compatibility.
The canonical location for these types is waypoint/types/proxy/policy_engine/.
"""

# Re-export all types from the new location
from waypoint.types.proxy.policy_engine import (  # Policy types; Validation types; Resolver types
    Policy,
    PolicyConfig,
    PolicyGuardrails,
    PolicyMatchContext,
    PolicyScope,
    PolicyValidateRequest,
    PolicyValidationError,
    PolicyValidationErrorType,
    PolicyValidationResponse,
    ResolvedPolicy,
)

__all__ = [
    # Policy types
    "Policy",
    "PolicyConfig",
    "PolicyGuardrails",
    # Resolver types
    "PolicyMatchContext",
    "PolicyScope",
    # Validation types
    "PolicyValidateRequest",
    "PolicyValidationError",
    "PolicyValidationErrorType",
    "PolicyValidationResponse",
    "ResolvedPolicy",
]
