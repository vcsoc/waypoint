from waypoint.types.utils import Usage
from waypoint.waypoint_core_utils.llm_cost_calc.utils import generic_cost_per_token


def cost_per_token(model: str, usage: Usage) -> tuple[float, float]:
    return generic_cost_per_token(model=model, usage=usage, custom_llm_provider="tencent")
