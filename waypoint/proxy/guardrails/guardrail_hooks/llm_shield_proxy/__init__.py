from typing import TYPE_CHECKING, Final

from waypoint.types.guardrails import SupportedGuardrailIntegrations

from .llm_shield_proxy import LLMShieldProxyGuardrail

if TYPE_CHECKING:
    from waypoint.types.guardrails import Guardrail, LitellmParams


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail") -> LLMShieldProxyGuardrail:
    import waypoint

    _llm_shield_guardrail_callback: Final = LLMShieldProxyGuardrail(
        api_key=litellm_params.api_key,
        api_base=litellm_params.api_base,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )

    waypoint.logging_callback_manager.add_litellm_callback(_llm_shield_guardrail_callback)
    return _llm_shield_guardrail_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.LLM_SHIELD_PROXY.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.LLM_SHIELD_PROXY.value: LLMShieldProxyGuardrail,
}
