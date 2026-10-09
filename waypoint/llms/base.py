## This is a template base class to be used for adding new LLM providers via API calls
from typing import TYPE_CHECKING, Any, Union

import httpx

import waypoint

if TYPE_CHECKING:
    from waypoint.types.utils import ModelResponse, TextCompletionResponse
    from waypoint.waypoint_core_utils.streaming_handler import CustomStreamWrapper
    from waypoint.waypoint_core_utils.waypoint_logging import Logging as LiteLLMLoggingObj


class BaseLLM:
    _client_session: httpx.Client | None = None

    def process_response(
        self,
        model: str,
        response: httpx.Response,
        model_response: "ModelResponse",
        stream: bool,
        logging_obj: "LiteLLMLoggingObj",
        optional_params: dict,
        api_key: str,
        data: dict | str,
        messages: list,
        print_verbose,
        encoding,
    ) -> Union["ModelResponse", "CustomStreamWrapper"]:
        """
        Helper function to process the response across sync + async completion calls
        """
        return model_response

    def process_text_completion_response(
        self,
        model: str,
        response: httpx.Response,
        model_response: "TextCompletionResponse",
        stream: bool,
        logging_obj: "LiteLLMLoggingObj",
        optional_params: dict,
        api_key: str,
        data: dict | str,
        messages: list,
        print_verbose,
        encoding,
    ) -> Union["TextCompletionResponse", "CustomStreamWrapper"]:
        """
        Helper function to process the response across sync + async completion calls
        """
        return model_response

    def create_client_session(self):
        if waypoint.client_session:
            _client_session = waypoint.client_session
        else:
            _client_session = httpx.Client()

        return _client_session

    def create_aclient_session(self):
        if waypoint.aclient_session:
            _aclient_session = waypoint.aclient_session
        else:
            _aclient_session = httpx.AsyncClient()

        return _aclient_session

    def __exit__(self):
        if hasattr(self, "_client_session") and self._client_session is not None:
            self._client_session.close()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, "_aclient_session"):
            await self._aclient_session.aclose()

    def validate_environment(self, *args, **kwargs) -> Any | None:  # set up the environment required to run the model
        return None

    def completion(self, *args, **kwargs) -> Any:  # logic for parsing in - calling - parsing out model completion calls
        return None

    def embedding(self, *args, **kwargs) -> Any:  # logic for parsing in - calling - parsing out model embedding calls
        return None
