"""
Unit test for Waypoint Proxy Responses API configuration.
"""

from waypoint.types.utils import LlmProviders


def test_litellm_proxy_responses_api_config_inherits_from_openai():
    """Test that LiteLLMProxyResponsesAPIConfig extends OpenAI config properly"""
    from waypoint.llms.waypoint_proxy.responses.transformation import (
        LiteLLMProxyResponsesAPIConfig,
    )
    from waypoint.llms.openai.responses.transformation import (
        OpenAIResponsesAPIConfig,
    )

    config = LiteLLMProxyResponsesAPIConfig()

    assert isinstance(config, OpenAIResponsesAPIConfig)

    assert config.custom_llm_provider == LlmProviders.LITELLM_PROXY
