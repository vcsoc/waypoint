import asyncio
import httpx
import json
import pytest
from typing import Any, Dict, List
from unittest.mock import MagicMock, Mock, patch
import os

import waypoint
from waypoint import embedding
from waypoint.exceptions import BadRequestError
from waypoint.llms.custom_httpx.http_handler import AsyncHTTPHandler, HTTPHandler
from waypoint.utils import (
    CustomStreamWrapper,
    get_supported_openai_params,
    get_optional_params,
    get_optional_params_embeddings,
)
import base64
from pathlib import Path

from abc import ABC, abstractmethod

file_data = (Path(__file__).parent.parent / "white_100x100.png").read_bytes()

encoded_file = base64.b64encode(file_data).decode("utf-8")
base64_image = f"data:image/png;base64,{encoded_file}"


class BaseLLMEmbeddingTest(ABC):
    """
    Abstract base test class that enforces a common test across all test classes.
    """

    @abstractmethod
    def get_base_embedding_call_args(self) -> dict:
        """Must return the base embedding call args"""
        pass

    @abstractmethod
    def get_custom_llm_provider(self) -> waypoint.LlmProviders:
        """Must return the custom llm provider"""
        pass

    @pytest.mark.asyncio()
    @pytest.mark.parametrize("sync_mode", [True, False])
    async def test_basic_embedding(self, sync_mode):
        waypoint.set_verbose = True
        embedding_call_args = self.get_base_embedding_call_args()
        if sync_mode is True:
            response = waypoint.embedding(
                **embedding_call_args,
                input=["hello", "world"],
            )

            print("embedding response: ", response)
        else:
            response = await waypoint.aembedding(
                **embedding_call_args,
                input=["hello", "world"],
            )

            print("async embedding response: ", response)

        from openai.types.create_embedding_response import CreateEmbeddingResponse

        CreateEmbeddingResponse.model_validate(response.model_dump())

    def test_embedding_optional_params_max_retries(self):
        embedding_call_args = self.get_base_embedding_call_args()
        optional_params = get_optional_params_embeddings(
            **embedding_call_args, max_retries=20
        )
        assert optional_params["max_retries"] == 20

    def test_image_embedding(self):
        waypoint.set_verbose = True
        from waypoint.utils import supports_embedding_image_input

        os.environ["WAYPOINT_LOCAL_MODEL_COST_MAP"] = "True"
        waypoint.model_cost = waypoint.get_model_cost_map(url="")

        base_embedding_call_args = self.get_base_embedding_call_args()
        if not supports_embedding_image_input(base_embedding_call_args["model"], None):
            print("Model does not support embedding image input")
            pytest.skip("Model does not support embedding image input")

        embedding(**base_embedding_call_args, input=[base64_image])
