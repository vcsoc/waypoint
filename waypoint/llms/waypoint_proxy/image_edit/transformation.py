from waypoint.llms.openai.image_edit.transformation import OpenAIImageEditConfig
from waypoint.secret_managers.main import get_secret_str


class LiteLLMProxyImageEditConfig(OpenAIImageEditConfig):
    """Configuration for image edit requests routed through Waypoint Proxy."""

    def validate_environment(
        self,
        headers: dict,
        model: str,
        api_key: str | None = None,
        litellm_params: dict | None = None,
        api_base: str | None = None,
    ) -> dict:
        api_key = api_key or get_secret_str("WAYPOINT_PROXY_API_KEY")
        headers.update({"Authorization": f"Bearer {api_key}"})
        return headers

    def get_complete_url(self, model: str, api_base: str | None, litellm_params: dict) -> str:
        api_base = api_base or get_secret_str("WAYPOINT_PROXY_API_BASE")
        if api_base is None:
            raise ValueError("api_base not set for Waypoint Proxy route. Set in env via `WAYPOINT_PROXY_API_BASE`")
        api_base = api_base.rstrip("/")
        return f"{api_base}/images/edits"
