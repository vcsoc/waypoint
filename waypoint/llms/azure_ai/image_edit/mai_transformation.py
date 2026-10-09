from typing import TYPE_CHECKING, Any, Final

import httpx
from httpx._types import RequestFiles

from waypoint.llms.azure_ai.common_utils import (
    AzureFoundryModelInfo,
    get_azure_ai_auth_headers,
)
from waypoint.llms.azure_ai.image_generation.mai_transformation import (
    AzureFoundryMAIImageGenerationConfig,
)
from waypoint.llms.openai.common_utils import OpenAIError
from waypoint.llms.openai.image_edit.transformation import OpenAIImageEditConfig
from waypoint.secret_managers.main import get_secret_str
from waypoint.types.llms.openai import FileTypes
from waypoint.types.router import GenericLiteLLMParams
from waypoint.types.utils import ImageResponse
from waypoint.utils import convert_to_model_response_object

if TYPE_CHECKING:
    from waypoint.waypoint_core_utils.logging import Logging as LiteLLMLoggingObj


class AzureFoundryMAIImageEditConfig(OpenAIImageEditConfig):
    """Azure AI Foundry MAI image editing (e.g. MAI-Image-2.5)."""

    def get_supported_openai_params(self, model: str) -> list:
        return ["prompt", "image", "model", "n"]

    def validate_environment(
        self,
        headers: dict,
        model: str,
        api_key: str | None = None,
        litellm_params: dict | None = None,
        api_base: str | None = None,
    ) -> dict:
        headers.update(
            get_azure_ai_auth_headers(
                api_key=AzureFoundryModelInfo.get_api_key(api_key),
                litellm_params=litellm_params,
                api_key_header="api-key",
            )
        )
        return headers

    def get_complete_url(
        self,
        model: str,
        api_base: str | None,
        litellm_params: dict,
    ) -> str:
        api_base = AzureFoundryModelInfo.get_api_base(api_base)

        if api_base is None:
            raise ValueError(
                "Azure AI API base is required. Set AZURE_AI_API_BASE environment variable or pass api_base parameter."
            )

        api_version: Final = litellm_params.get("api_version") or get_secret_str("AZURE_AI_API_VERSION") or "preview"

        return AzureFoundryMAIImageGenerationConfig.get_mai_image_edit_url(
            api_base=api_base,
            api_version=api_version,
        )

    def transform_image_edit_request(
        self,
        model: str,
        prompt: str | None,
        image: FileTypes | None,
        image_edit_optional_request_params: dict,
        litellm_params: GenericLiteLLMParams,
        headers: dict,
    ) -> tuple[dict, RequestFiles]:
        request_params: Final = {
            "model": model,
            **image_edit_optional_request_params,
        }
        if prompt is not None:
            request_params["prompt"] = prompt

        data_without_files = {key: value for key, value in request_params.items() if key not in ["image", "mask"]}
        files_list: Final[list[tuple[str, Any]]] = []

        if image is not None:
            image_list: Final = [image] if not isinstance(image, list) else image
            for _image in image_list:
                if _image is not None:
                    self._add_image_to_files(
                        files_list=files_list,
                        image=_image,
                        field_name="image",
                    )
                    break

        return data_without_files, files_list

    def transform_image_edit_response(
        self,
        model: str,
        raw_response: httpx.Response,
        logging_obj: "LiteLLMLoggingObj",
    ) -> ImageResponse:
        try:
            response: Final = raw_response.json()
        except Exception:
            raise OpenAIError(message=raw_response.text, status_code=raw_response.status_code)

        if "usage" in response:
            response["usage"] = AzureFoundryMAIImageGenerationConfig.normalize_mai_image_usage(response.get("usage"))

        logging_obj.post_call(
            input="",
            api_key="",
            additional_args={"complete_input_dict": {}},
            original_response=response,
        )

        return convert_to_model_response_object(
            response_object=response,
            model_response_object=ImageResponse(),
            response_type="image_generation",
        )
