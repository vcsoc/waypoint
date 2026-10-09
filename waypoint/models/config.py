"""
Config table model.

Canonical definition for ``litellm_config``. Re-exported from
``waypoint.proxy._types`` for backwards compatibility.
"""

from waypoint.types.llms.base import LiteLLMPydanticObjectBase


class LiteLLM_Config(LiteLLMPydanticObjectBase):
    param_name: str
    param_value: dict
