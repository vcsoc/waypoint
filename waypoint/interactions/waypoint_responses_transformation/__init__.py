"""
Bridge module for connecting Interactions API to Responses API via waypoint.responses().
"""

from waypoint.interactions.waypoint_responses_transformation.handler import (
    LiteLLMResponsesInteractionsHandler,
)
from waypoint.interactions.waypoint_responses_transformation.transformation import (
    LiteLLMResponsesInteractionsConfig,
)

__all__ = [
    "LiteLLMResponsesInteractionsConfig",  # Transformation config class (not BaseInteractionsAPIConfig)
    "LiteLLMResponsesInteractionsHandler",
]
