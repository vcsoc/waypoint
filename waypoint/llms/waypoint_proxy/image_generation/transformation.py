from waypoint.llms.openai.image_generation.gpt_transformation import (
    GPTImageGenerationConfig,
)
from waypoint.secret_managers.main import get_secret_str


class LiteLLMProxyImageGenerationConfig(GPTImageGenerationConfig):
    """Configuration for image generation requests routed through Waypoint Proxy."""

    def validate_environment(
        self,
        headers: dict,
        model: str,
        messages,
        optional_params: dict,
        litellm_params: dict,
        api_key: str | None = None,
        api_base: str | None = None,
    ) -> dict:
        api_key = api_key or get_secret_str("WAYPOINT_PROXY_API_KEY")
        headers.update({"Authorization": f"Bearer {api_key}"})
        return headers

    def get_complete_url(
        self,
        api_base: str | None,
        api_key: str | None,
        model: str,
        optional_params: dict,
        litellm_params: dict,
        stream: bool | None = None,
    ) -> str:
        api_base = api_base or get_secret_str("WAYPOINT_PROXY_API_BASE")
        if api_base is None:
            raise ValueError("api_base not set for Waypoint Proxy route. Set in env via `WAYPOINT_PROXY_API_BASE`")
        api_base = api_base.rstrip("/")
        return f"{api_base}/images/generations"
