### What this tests ####
## This test asserts the type of data passed into each method of the custom callback handler
import asyncio
import inspect
import os
import traceback
from datetime import datetime
from typing import List, Literal, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import BaseModel

import waypoint
from waypoint import Cache
from waypoint.integrations.custom_logger import CustomLogger
from waypoint.types.utils import LiteLLMCommonStrings
from tests._wait_helpers import await_until, wait_until

# Test Scenarios (test across completion, streaming, embedding)
## 1: Pre-API-Call
## 2: Post-API-Call
## 3: On Waypoint Call success
## 4: On Waypoint Call failure
## 5. Caching

# Test models
## 1. OpenAI
## 2. Azure OpenAI
## 3. Non-OpenAI/Azure - e.g. Bedrock

# Test interfaces
## 1. waypoint.completion() + waypoint.embeddings()
## refer to test_custom_callback_input_router.py for the router +  proxy tests


class CompletionCustomHandler(
    CustomLogger
):  # https://docs.litellm.ai/docs/observability/custom_callback#callback-class
    """
    The set of expected inputs to a custom handler for a
    """

    # Class variables or attributes
    def __init__(self):
        self.errors = []
        self.states: List[
            Literal[
                "sync_pre_api_call",
                "async_pre_api_call",
                "post_api_call",
                "sync_stream",
                "async_stream",
                "sync_success",
                "async_success",
                "sync_failure",
                "async_failure",
            ]
        ] = []

    def log_pre_api_call(self, model, messages, kwargs):
        try:
            self.states.append("sync_pre_api_call")
            ## MODEL
            assert isinstance(model, str)
            ## MESSAGES
            assert isinstance(messages, list)
            ## KWARGS
            assert isinstance(kwargs["model"], str)
            assert isinstance(kwargs["messages"], list)
            assert isinstance(kwargs["optional_params"], dict)
            assert isinstance(kwargs["litellm_params"], dict)
            assert isinstance(kwargs["start_time"], (datetime, type(None)))
            assert isinstance(kwargs["stream"], bool)
            assert isinstance(kwargs["user"], (str, type(None)))
            ### METADATA
            metadata_value = kwargs["litellm_params"].get("metadata")
            assert metadata_value is None or isinstance(metadata_value, dict)
            if metadata_value is not None:
                if waypoint.turn_off_message_logging is True:
                    assert (
                        metadata_value["raw_request"]
                        is LiteLLMCommonStrings.redacted_by_litellm.value
                    )
                else:
                    assert "raw_request" not in metadata_value or isinstance(
                        metadata_value["raw_request"], str
                    )
        except Exception:
            print(f"Assertion Error: {traceback.format_exc()}")
            self.errors.append(traceback.format_exc())

    def log_post_api_call(self, kwargs, response_obj, start_time, end_time):
        try:
            self.states.append("post_api_call")
            ## START TIME
            assert isinstance(start_time, datetime)
            ## END TIME
            assert end_time == None
            ## RESPONSE OBJECT
            assert response_obj == None
            ## KWARGS
            assert isinstance(kwargs["model"], str)
            assert isinstance(kwargs["messages"], list)
            assert isinstance(kwargs["optional_params"], dict)
            assert isinstance(kwargs["litellm_params"], dict)
            assert isinstance(kwargs["start_time"], (datetime, type(None)))
            assert isinstance(kwargs["stream"], bool)
            assert isinstance(kwargs["user"], (str, type(None)))
            assert isinstance(kwargs["input"], (list, dict, str))
            assert isinstance(kwargs["api_key"], (str, type(None)))
            assert (
                isinstance(
                    kwargs["original_response"],
                    (str, waypoint.CustomStreamWrapper, BaseModel),
                )
                or inspect.iscoroutine(kwargs["original_response"])
                or inspect.isasyncgen(kwargs["original_response"])
            )
            assert isinstance(kwargs["additional_args"], (dict, type(None)))
            assert isinstance(kwargs["log_event_type"], str)
        except Exception:
            print(f"Assertion Error: {traceback.format_exc()}")
            self.errors.append(traceback.format_exc())

    async def async_log_stream_event(self, kwargs, response_obj, start_time, end_time):
        try:
            self.states.append("async_stream")
            ## START TIME
            assert isinstance(start_time, datetime)
            ## END TIME
            assert isinstance(end_time, datetime)
            ## RESPONSE OBJECT
            assert isinstance(response_obj, waypoint.ModelResponseStream)
            ## KWARGS
            assert isinstance(kwargs["model"], str)
            assert isinstance(kwargs["messages"], list) and isinstance(
                kwargs["messages"][0], dict
            )
            assert isinstance(kwargs["optional_params"], dict)
            assert isinstance(kwargs["litellm_params"], dict)
            assert isinstance(kwargs["start_time"], (datetime, type(None)))
            assert isinstance(kwargs["stream"], bool)
            assert isinstance(kwargs["user"], (str, type(None)))
            assert (
                isinstance(kwargs["input"], list)
                and isinstance(kwargs["input"][0], dict)
            ) or isinstance(kwargs["input"], (dict, str))
            assert isinstance(kwargs["api_key"], (str, type(None)))
            assert (
                isinstance(
                    kwargs["original_response"], (str, waypoint.CustomStreamWrapper)
                )
                or inspect.isasyncgen(kwargs["original_response"])
                or inspect.iscoroutine(kwargs["original_response"])
            )
            assert isinstance(kwargs["additional_args"], (dict, type(None)))
            assert isinstance(kwargs["log_event_type"], str)
        except Exception:
            print(f"Assertion Error: {traceback.format_exc()}")
            self.errors.append(traceback.format_exc())

    def log_success_event(self, kwargs, response_obj, start_time, end_time):
        try:
            print(f"\n\nkwargs={kwargs}\n\n")
            print(
                json.dumps(kwargs, default=str)
            )  # this is a test to confirm no circular references are in the logging object

            self.states.append("sync_success")
            ## START TIME
            assert isinstance(start_time, datetime)
            ## END TIME
            assert isinstance(end_time, datetime)
            ## RESPONSE OBJECT
            assert isinstance(
                response_obj,
                (
                    waypoint.ModelResponse,
                    waypoint.EmbeddingResponse,
                    waypoint.ImageResponse,
                ),
            )
            ## KWARGS
            assert isinstance(kwargs["model"], str)
            assert isinstance(kwargs["messages"], list) and isinstance(
                kwargs["messages"][0], dict
            )
            assert isinstance(kwargs["optional_params"], dict)
            assert isinstance(kwargs["litellm_params"], dict)
            assert isinstance(kwargs["litellm_params"]["api_base"], str)
            assert kwargs["cache_hit"] is None or isinstance(kwargs["cache_hit"], bool)
            assert isinstance(kwargs["start_time"], (datetime, type(None)))
            assert isinstance(kwargs["stream"], bool)
            assert isinstance(kwargs["user"], (str, type(None)))
            assert (
                isinstance(kwargs["input"], list)
                and (
                    isinstance(kwargs["input"][0], dict)
                    or isinstance(kwargs["input"][0], str)
                )
            ) or isinstance(kwargs["input"], (dict, str))
            assert isinstance(kwargs["api_key"], (str, type(None)))
            assert isinstance(
                kwargs["original_response"],
                (str, waypoint.CustomStreamWrapper, BaseModel),
            ), "Original Response={}. Allowed types=[str, waypoint.CustomStreamWrapper, BaseModel]".format(
                kwargs["original_response"]
            )
            assert isinstance(kwargs["additional_args"], (dict, type(None)))
            assert isinstance(kwargs["log_event_type"], str)
            assert isinstance(kwargs["response_cost"], (float, type(None)))
        except Exception:
            print(f"Assertion Error: {traceback.format_exc()}")
            self.errors.append(traceback.format_exc())

    def log_failure_event(self, kwargs, response_obj, start_time, end_time):
        try:
            print(f"kwargs: {kwargs}")
            self.states.append("sync_failure")
            ## START TIME
            assert isinstance(start_time, datetime)
            ## END TIME
            assert isinstance(end_time, datetime)
            ## RESPONSE OBJECT
            assert response_obj == None
            ## KWARGS
            assert isinstance(kwargs["model"], str)
            assert isinstance(kwargs["messages"], list) and isinstance(
                kwargs["messages"][0], dict
            )

            assert isinstance(kwargs["optional_params"], dict)
            assert isinstance(kwargs["litellm_params"], dict)
            assert isinstance(kwargs["litellm_params"]["metadata"], Optional[dict])
            assert isinstance(kwargs["start_time"], (datetime, type(None)))
            assert isinstance(kwargs["stream"], bool)
            assert isinstance(kwargs["user"], (str, type(None)))
            assert (
                isinstance(kwargs["input"], list)
                and isinstance(kwargs["input"][0], dict)
            ) or isinstance(kwargs["input"], (dict, str))
            assert isinstance(kwargs["api_key"], (str, type(None)))
            assert (
                isinstance(
                    kwargs["original_response"], (str, waypoint.CustomStreamWrapper)
                )
                or kwargs["original_response"] == None
            )
            assert isinstance(kwargs["additional_args"], (dict, type(None)))
            assert isinstance(kwargs["log_event_type"], str)
        except Exception:
            print(f"Assertion Error: {traceback.format_exc()}")
            self.errors.append(traceback.format_exc())

    async def async_log_pre_api_call(self, model, messages, kwargs):
        try:
            self.states.append("async_pre_api_call")
            ## MODEL
            assert isinstance(model, str)
            ## MESSAGES
            assert isinstance(messages, list) and isinstance(messages[0], dict)
            ## KWARGS
            assert isinstance(kwargs["model"], str)
            assert isinstance(kwargs["messages"], list) and isinstance(
                kwargs["messages"][0], dict
            )
            assert isinstance(kwargs["optional_params"], dict)
            assert isinstance(kwargs["litellm_params"], dict)
            assert isinstance(kwargs["start_time"], (datetime, type(None)))
            assert isinstance(kwargs["stream"], bool)
            assert isinstance(kwargs["user"], (str, type(None)))
        except Exception as e:
            print(f"Assertion Error: {traceback.format_exc()}")
            self.errors.append(traceback.format_exc())

    async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):
        try:
            print(
                "in async_log_success_event", kwargs, response_obj, start_time, end_time
            )
            self.states.append("async_success")
            ## START TIME
            assert isinstance(start_time, datetime)
            ## END TIME
            assert isinstance(end_time, datetime)
            ## RESPONSE OBJECT
            assert isinstance(
                response_obj,
                (
                    waypoint.ModelResponse,
                    waypoint.EmbeddingResponse,
                    waypoint.TextCompletionResponse,
                ),
            )
            ## KWARGS
            assert isinstance(kwargs["model"], str)
            assert isinstance(kwargs["messages"], list)
            assert isinstance(kwargs["optional_params"], dict)
            assert isinstance(kwargs["litellm_params"], dict)
            assert isinstance(kwargs["litellm_params"]["api_base"], str)
            assert isinstance(kwargs["start_time"], (datetime, type(None)))
            assert isinstance(kwargs["stream"], bool)
            assert isinstance(kwargs["completion_start_time"], datetime)
            assert kwargs["cache_hit"] is None or isinstance(kwargs["cache_hit"], bool)
            assert isinstance(kwargs["user"], (str, type(None)))
            assert isinstance(kwargs["input"], (list, dict, str))
            assert isinstance(kwargs["api_key"], (str, type(None)))
            assert (
                isinstance(
                    kwargs["original_response"], (str, waypoint.CustomStreamWrapper)
                )
                or inspect.isasyncgen(kwargs["original_response"])
                or inspect.iscoroutine(kwargs["original_response"])
            )
            assert isinstance(kwargs["additional_args"], (dict, type(None)))
            assert isinstance(kwargs["log_event_type"], str)
            assert kwargs["cache_hit"] is None or isinstance(kwargs["cache_hit"], bool)
            assert isinstance(kwargs["response_cost"], (float, type(None)))
        except Exception:
            print(f"Assertion Error: {traceback.format_exc()}")
            self.errors.append(traceback.format_exc())

    async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time):
        try:
            self.states.append("async_failure")
            ## START TIME
            assert isinstance(start_time, datetime)
            ## END TIME
            assert isinstance(end_time, datetime)
            ## RESPONSE OBJECT
            assert response_obj == None
            ## KWARGS
            assert isinstance(kwargs["model"], str)
            assert isinstance(kwargs["messages"], list)
            assert isinstance(kwargs["optional_params"], dict)
            assert isinstance(kwargs["litellm_params"], dict)
            assert isinstance(kwargs["start_time"], (datetime, type(None)))
            assert isinstance(kwargs["stream"], bool)
            assert isinstance(kwargs["user"], (str, type(None)))
            assert isinstance(kwargs["input"], (list, str, dict))
            assert isinstance(kwargs["api_key"], (str, type(None)))
            assert (
                isinstance(
                    kwargs["original_response"], (str, waypoint.CustomStreamWrapper)
                )
                or inspect.isasyncgen(kwargs["original_response"])
                or inspect.iscoroutine(kwargs["original_response"])
                or kwargs["original_response"] == None
            )
            assert isinstance(kwargs["additional_args"], (dict, type(None)))
            assert isinstance(kwargs["log_event_type"], str)
        except Exception:
            print(f"Assertion Error: {traceback.format_exc()}")
            self.errors.append(traceback.format_exc())


# COMPLETION
## Test OpenAI + sync
def test_chat_openai_stream():
    try:
        customHandler = CompletionCustomHandler()
        waypoint.callbacks = [customHandler]
        response = waypoint.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi 👋 - i'm sync openai"}],
        )
        ## test streaming
        response = waypoint.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi 👋 - i'm openai"}],
            stream=True,
        )
        for chunk in response:
            continue
        ## test failure callback
        try:
            response = waypoint.completion(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hi 👋 - i'm openai"}],
                api_key="my-bad-key",
                stream=True,
            )
            for chunk in response:
                continue
        except Exception:
            pass
        wait_until(
            lambda: "sync_failure" in customHandler.states,
            message=f"no sync_failure callback, states={customHandler.states}",
        )
        print(f"customHandler.errors: {customHandler.errors}")
        assert len(customHandler.errors) == 0
        waypoint.callbacks = []
    except Exception as e:
        pytest.fail(f"An exception occurred: {str(e)}")


# test_chat_openai_stream()


## Test OpenAI + Async
@pytest.mark.asyncio
async def test_async_chat_openai_stream():
    try:
        customHandler = CompletionCustomHandler()
        waypoint.callbacks = [customHandler]
        response = await waypoint.acompletion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi 👋 - i'm openai"}],
        )
        ## test streaming
        response = await waypoint.acompletion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi 👋 - i'm openai"}],
            stream=True,
        )
        async for chunk in response:
            continue

        await asyncio.sleep(1)
        ## test failure callback
        try:
            response = await waypoint.acompletion(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hi 👋 - i'm openai"}],
                api_key="my-bad-key",
                stream=True,
            )
            async for chunk in response:
                continue
        except Exception:
            pass
        await await_until(
            lambda: "async_failure" in customHandler.states,
            message=f"no async_failure callback, states={customHandler.states}",
        )
        print(f"customHandler.errors: {customHandler.errors}")
        assert len(customHandler.errors) == 0
        waypoint.callbacks = []
    except Exception as e:
        pytest.fail(f"An exception occurred: {str(e)}")


# asyncio.run(test_async_chat_openai_stream())


## Test Azure + sync
def test_chat_azure_stream():
    try:
        customHandler = CompletionCustomHandler()
        waypoint.callbacks = [customHandler]
        response = waypoint.completion(
            model="azure/gpt-4.1-mini",
            messages=[{"role": "user", "content": "Hi 👋 - i'm sync azure"}],
        )
        # test streaming
        response = waypoint.completion(
            model="azure/gpt-4.1-mini",
            messages=[{"role": "user", "content": "Hi 👋 - i'm sync azure"}],
            stream=True,
        )
        for chunk in response:
            continue
        # test failure callback
        try:
            response = waypoint.completion(
                model="azure/gpt-4.1-mini",
                messages=[{"role": "user", "content": "Hi 👋 - i'm sync azure"}],
                api_key="my-bad-key",
                stream=True,
            )
            for chunk in response:
                continue
        except Exception:
            pass
        wait_until(
            lambda: "sync_failure" in customHandler.states,
            message=f"no sync_failure callback, states={customHandler.states}",
        )
        print(f"customHandler.errors: {customHandler.errors}")
        assert len(customHandler.errors) == 0
        waypoint.callbacks = []
    except Exception as e:
        pytest.fail(f"An exception occurred: {str(e)}")


# test_chat_azure_stream()


## Test Azure + Async
@pytest.mark.asyncio
async def test_async_chat_azure_stream():
    try:
        customHandler = CompletionCustomHandler()
        waypoint.callbacks = [customHandler]
        response = await waypoint.acompletion(
            model="azure/gpt-4.1-mini",
            messages=[{"role": "user", "content": "Hi 👋 - i'm async azure"}],
        )
        ## test streaming
        response = await waypoint.acompletion(
            model="azure/gpt-4.1-mini",
            messages=[{"role": "user", "content": "Hi 👋 - i'm async azure"}],
            stream=True,
        )
        async for chunk in response:
            continue

        await asyncio.sleep(1)
        # test failure callback
        try:
            response = await waypoint.acompletion(
                model="azure/gpt-4.1-mini",
                messages=[{"role": "user", "content": "Hi 👋 - i'm async azure"}],
                api_key="my-bad-key",
                stream=True,
            )
            async for chunk in response:
                continue
            await asyncio.sleep(1)
        except Exception:
            pass
        await asyncio.sleep(1)
        print(f"customHandler.errors: {customHandler.errors}")
        assert len(customHandler.errors) == 0
        waypoint.callbacks = []
    except Exception as e:
        pytest.fail(f"An exception occurred: {str(e)}")


# asyncio.run(test_async_chat_azure_stream())


@pytest.mark.asyncio
async def test_async_chat_openai_stream_options():
    try:
        waypoint.set_verbose = True
        customHandler = CompletionCustomHandler()
        waypoint.callbacks = [customHandler]
        with patch.object(
            customHandler, "async_log_success_event", new=AsyncMock()
        ) as mock_client:
            response = await waypoint.acompletion(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hi 👋 - i'm async openai"}],
                stream=True,
                stream_options={"include_usage": True},
            )

            async for chunk in response:
                continue

            await asyncio.sleep(1)
            print("mock client args list=", mock_client.await_args_list)
            mock_client.assert_awaited_once()
    except Exception as e:
        pytest.fail(f"An exception occurred: {str(e)}")


# asyncio.run(test_async_chat_bedrock_stream())


## Test Sagemaker + Async


## Test Vertex AI + Async
import json

# Text Completion




## Test OpenAI text completion + Async
@pytest.mark.asyncio
async def test_async_text_completion_openai_stream():
    try:
        customHandler = CompletionCustomHandler()
        waypoint.callbacks = [customHandler]
        response = await waypoint.atext_completion(
            model="gpt-3.5-turbo",
            prompt="Hi 👋 - i'm async text completion openai",
        )
        # test streaming
        response = await waypoint.atext_completion(
            model="gpt-3.5-turbo",
            prompt="Hi 👋 - i'm async text completion openai",
            stream=True,
        )
        async for chunk in response:
            print(f"chunk: {chunk}")
            continue

        await asyncio.sleep(1)
        ## test failure callback
        try:
            response = await waypoint.atext_completion(
                model="gpt-3.5-turbo",
                prompt="Hi 👋 - i'm async text completion openai",
                stream=True,
                api_key="my-bad-key",
            )
            async for chunk in response:
                continue

        except Exception:
            pass
        await await_until(
            lambda: "async_failure" in customHandler.states,
            message=f"no async_failure callback, states={customHandler.states}",
        )
        print(f"customHandler.errors: {customHandler.errors}")
        assert len(customHandler.errors) == 0
        waypoint.callbacks = []
    except Exception as e:
        pytest.fail(f"An exception occurred: {str(e)}")


# EMBEDDING
## Test OpenAI + Async
@pytest.mark.asyncio
async def test_async_embedding_openai():
    try:
        customHandler_success = CompletionCustomHandler()
        customHandler_failure = CompletionCustomHandler()
        waypoint.callbacks = [customHandler_success]
        response = await waypoint.aembedding(
            model="text-embedding-ada-002",
            input=["good morning from waypoint"],
        )
        await asyncio.sleep(1)
        print(f"customHandler_success.errors: {customHandler_success.errors}")
        print(f"customHandler_success.states: {customHandler_success.states}")
        assert len(customHandler_success.errors) == 0
        assert len(customHandler_success.states) == 3  # pre, post, success
        # test failure callback
        waypoint.logging_callback_manager._reset_all_callbacks()
        waypoint.callbacks = [customHandler_failure]
        try:
            response = await waypoint.aembedding(
                model="text-embedding-ada-002",
                input=["good morning from waypoint"],
                api_key="my-bad-key",
            )
        except Exception:
            pass
        await asyncio.sleep(1)
        print(f"customHandler_failure.errors: {customHandler_failure.errors}")
        print(f"customHandler_failure.states: {customHandler_failure.states}")
        assert len(customHandler_failure.errors) == 0
        assert len(customHandler_failure.states) == 3  # pre, post, failure
    except Exception as e:
        pytest.fail(f"An exception occurred: {str(e)}")


# asyncio.run(test_async_embedding_openai())


## Test Azure + Async
def test_amazing_sync_embedding():
    try:
        customHandler_success = CompletionCustomHandler()
        customHandler_failure = CompletionCustomHandler()
        waypoint.callbacks = [customHandler_success]
        response = waypoint.embedding(
            model="azure/text-embedding-ada-002", input=["good morning from waypoint"]
        )
        print(f"customHandler_success.errors: {customHandler_success.errors}")
        print(f"customHandler_success.states: {customHandler_success.states}")
        wait_until(
            lambda: len(customHandler_success.states) == 3,
            message=f"success states never reached pre/post/success, got {customHandler_success.states}",
        )
        assert len(customHandler_success.errors) == 0
        assert len(customHandler_success.states) == 3  # pre, post, success
        # test failure callback
        waypoint.logging_callback_manager._reset_all_callbacks()
        waypoint.callbacks = [customHandler_failure]
        try:
            response = waypoint.embedding(
                model="azure/text-embedding-ada-002",
                input=["good morning from waypoint"],
                api_key="my-bad-key",
            )
        except Exception:
            pass
        print(f"customHandler_failure.errors: {customHandler_failure.errors}")
        print(f"customHandler_failure.states: {customHandler_failure.states}")
        wait_until(
            lambda: len(customHandler_failure.states) == 3,
            message=f"failure states never reached pre/post/failure, got {customHandler_failure.states}",
        )
        assert len(customHandler_failure.errors) == 1
        assert len(customHandler_failure.states) == 3  # pre, post, failure
    except Exception as e:
        pytest.fail(f"An exception occurred: {str(e)}")


## Test Azure + Async
@pytest.mark.asyncio
async def test_async_embedding_azure():
    try:
        customHandler_success = CompletionCustomHandler()
        customHandler_failure = CompletionCustomHandler()
        waypoint.callbacks = [customHandler_success]
        response = await waypoint.aembedding(
            model="azure/text-embedding-ada-002", input=["good morning from waypoint"]
        )
        await asyncio.sleep(1)
        print(f"customHandler_success.errors: {customHandler_success.errors}")
        print(f"customHandler_success.states: {customHandler_success.states}")
        assert len(customHandler_success.errors) == 0
        assert len(customHandler_success.states) == 3  # pre, post, success
        # test failure callback
        waypoint.logging_callback_manager._reset_all_callbacks()
        waypoint.callbacks = [customHandler_failure]
        try:
            response = await waypoint.aembedding(
                model="azure/text-embedding-ada-002",
                input=["good morning from waypoint"],
                api_key="my-bad-key",
            )
        except Exception:
            pass
        await asyncio.sleep(1)
        print(f"customHandler_failure.errors: {customHandler_failure.errors}")
        print(f"customHandler_failure.states: {customHandler_failure.states}")
        assert len(customHandler_failure.errors) == 0
        assert len(customHandler_failure.states) == 3  # pre, post, success
    except Exception as e:
        pytest.fail(f"An exception occurred: {str(e)}")


# asyncio.run(test_async_embedding_azure())


## Test Bedrock + Async
@pytest.mark.asyncio
async def test_async_embedding_bedrock():
    try:
        customHandler_success = CompletionCustomHandler()
        customHandler_failure = CompletionCustomHandler()
        waypoint.callbacks = [customHandler_success]
        waypoint.set_verbose = True
        response = await waypoint.aembedding(
            model="bedrock/cohere.embed-multilingual-v3",
            input=["good morning from waypoint"],
            aws_region_name="us-east-1",
        )
        await asyncio.sleep(1)
        print(f"customHandler_success.errors: {customHandler_success.errors}")
        print(f"customHandler_success.states: {customHandler_success.states}")
        assert len(customHandler_success.errors) == 0
        assert len(customHandler_success.states) == 3  # pre, post, success
        # test failure callback
        waypoint.logging_callback_manager._reset_all_callbacks()
        waypoint.callbacks = [customHandler_failure]
        try:
            response = await waypoint.aembedding(
                model="bedrock/cohere.embed-multilingual-v3",
                input=["good morning from waypoint"],
                aws_region_name="my-bad-region",
            )
        except Exception:
            pass
        await asyncio.sleep(1)
        print(f"customHandler_failure.errors: {customHandler_failure.errors}")
        print(f"customHandler_failure.states: {customHandler_failure.states}")
        assert len(customHandler_failure.errors) == 0
        assert len(customHandler_failure.states) == 3  # pre, post, success
    except Exception as e:
        pytest.fail(f"An exception occurred: {str(e)}")


# Image Generation


## Test OpenAI + Sync
@pytest.mark.flaky(retries=3, delay=1)
def test_image_generation_openai():
    try:
        customHandler_success = CompletionCustomHandler()
        customHandler_failure = CompletionCustomHandler()
        waypoint.callbacks = [customHandler_success]

        waypoint.set_verbose = True

        response = waypoint.image_generation(
            prompt="A cute baby sea otter",
            model="openai/gpt-image-1",
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        print(f"response: {response}")
        assert len(response.data) > 0

        print(f"customHandler_success.errors: {customHandler_success.errors}")
        print(f"customHandler_success.states: {customHandler_success.states}")
        wait_until(
            lambda: len(customHandler_success.states) == 3,
            message=f"success states never reached pre/post/success, got {customHandler_success.states}",
        )
        assert len(customHandler_success.errors) == 0
        assert len(customHandler_success.states) == 3  # pre, post, success
        # test failure callback
        waypoint.logging_callback_manager._reset_all_callbacks()
        waypoint.callbacks = [customHandler_failure]
        try:
            response = waypoint.image_generation(
                prompt="A cute baby sea otter",
                model="gpt-image-1",
                api_key="my-bad-api-key",
            )
        except Exception:
            pass
        print(f"customHandler_failure.errors: {customHandler_failure.errors}")
        print(f"customHandler_failure.states: {customHandler_failure.states}")
        assert len(customHandler_failure.errors) == 0
        assert len(customHandler_failure.states) == 3  # pre, post, failure
    except waypoint.RateLimitError as e:
        pass
    except waypoint.ContentPolicyViolationError:
        pass  # OpenAI randomly raises these errors - skip when they occur
    except Exception as e:
        pytest.fail(f"An exception occurred - {str(e)}")


# test_image_generation_openai()
## Test OpenAI + Async

## Test Azure + Sync

## Test Azure + Async

##### PII REDACTION ######


def test_turn_off_message_logging():
    """
    If 'turn_off_message_logging' is true, assert no user request information is logged.
    """
    waypoint.turn_off_message_logging = True

    # sync completion
    customHandler = CompletionCustomHandler()
    waypoint.callbacks = [customHandler]

    _ = waypoint.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hey, how's it going?"}],
        mock_response="Going well!",
    )

    wait_until(
        lambda: "sync_success" in customHandler.states,
        message=f"no sync_success callback, states={customHandler.states}",
    )
    assert len(customHandler.errors) == 0


##### VALID JSON ######


@pytest.mark.parametrize(
    "model",
    [
        "ft:gpt-3.5-turbo:my-org:custom_suffix:id"
    ],  # "gpt-3.5-turbo", "azure/gpt-4.1-mini",
)
@pytest.mark.parametrize(
    "turn_off_message_logging",
    [
        True,
    ],
)  # False
def test_standard_logging_payload(model, turn_off_message_logging):
    """
    Ensure valid standard_logging_payload is passed for logging calls to s3

    Motivation: provide a standard set of things that are logged to s3/gcs/future integrations across all llm calls
    """
    from waypoint.types.utils import StandardLoggingPayload

    # sync completion
    customHandler = CompletionCustomHandler()
    waypoint.callbacks = [customHandler]

    waypoint.turn_off_message_logging = turn_off_message_logging

    with patch.object(
        customHandler, "log_success_event", new=MagicMock()
    ) as mock_client:
        _ = waypoint.completion(
            model=model,
            messages=[{"role": "user", "content": "Hey, how's it going?"}],
            mock_response="Going well!",
        )

        wait_until(lambda: mock_client.called, message="log_success_event never fired")
        mock_client.assert_called_once()

        print(
            f"mock_client_post.call_args: {mock_client.call_args.kwargs['kwargs'].keys()}"
        )
        assert "standard_logging_object" in mock_client.call_args.kwargs["kwargs"]
        assert (
            mock_client.call_args.kwargs["kwargs"]["standard_logging_object"]
            is not None
        )

        print(
            "Standard Logging Object - {}".format(
                mock_client.call_args.kwargs["kwargs"]["standard_logging_object"]
            )
        )

        keys_list = list(StandardLoggingPayload.__required_keys__)

        for k in keys_list:
            assert (
                k in mock_client.call_args.kwargs["kwargs"]["standard_logging_object"]
            )

        ## json serializable
        json_str_payload = json.dumps(
            mock_client.call_args.kwargs["kwargs"]["standard_logging_object"]
        )
        json.loads(json_str_payload)

        ## response cost
        assert (
            mock_client.call_args.kwargs["kwargs"]["standard_logging_object"][
                "response_cost"
            ]
            > 0
        )
        assert (
            mock_client.call_args.kwargs["kwargs"]["standard_logging_object"][
                "model_map_information"
            ]["model_map_value"]
            is not None
        )

        ## turn off message logging
        slobject: StandardLoggingPayload = mock_client.call_args.kwargs["kwargs"][
            "standard_logging_object"
        ]
        if turn_off_message_logging:
            print("checks redacted-by-litellm")
            assert "redacted-by-litellm" == slobject["messages"][0]["content"]
            response = slobject["response"]
            if "choices" in response:
                assert (
                    response["choices"][0]["message"]["content"]
                    == "redacted-by-litellm"
                )
                assert response["choices"][0]["message"].get("audio") is None
            else:
                assert response["text"] == "redacted-by-litellm"


@pytest.mark.parametrize(
    "stream",
    [True, False],
)
@pytest.mark.parametrize(
    "turn_off_message_logging",
    [
        True,
    ],
)  # False
def test_standard_logging_payload_audio(turn_off_message_logging, stream):
    """
    Ensure valid standard_logging_payload is passed for logging calls to s3

    Motivation: provide a standard set of things that are logged to s3/gcs/future integrations across all llm calls
    """
    from waypoint.types.utils import StandardLoggingPayload

    # sync completion
    customHandler = CompletionCustomHandler()
    waypoint.callbacks = [customHandler]

    waypoint.turn_off_message_logging = turn_off_message_logging

    with patch.object(
        customHandler, "log_success_event", new=MagicMock()
    ) as mock_client:
        try:
            response = waypoint.completion(
                model="gpt-audio-1.5",
                modalities=["text", "audio"],
                audio={"voice": "alloy", "format": "pcm16"},
                messages=[
                    {"role": "user", "content": "response in 1 word - yes or no"}
                ],
                stream=stream,
            )
        except Exception as e:
            err = str(e).lower()
            if (
                "model_not_found" in err
                or "does not exist" in err
                or "openai-internal" in err
            ):
                pytest.skip(f"Skipping - upstream gpt-audio-1.5 unavailable: {e}")
            raise

        if stream:
            for chunk in response:
                continue

        wait_until(lambda: mock_client.called, message="log_success_event never fired")
        mock_client.assert_called()

        print(
            f"mock_client_post.call_args: {mock_client.call_args.kwargs['kwargs'].keys()}"
        )
        assert "standard_logging_object" in mock_client.call_args.kwargs["kwargs"]
        assert (
            mock_client.call_args.kwargs["kwargs"]["standard_logging_object"]
            is not None
        )

        print(
            "Standard Logging Object - {}".format(
                mock_client.call_args.kwargs["kwargs"]["standard_logging_object"]
            )
        )

        keys_list = list(StandardLoggingPayload.__required_keys__)

        for k in keys_list:
            assert (
                k in mock_client.call_args.kwargs["kwargs"]["standard_logging_object"]
            )

        ## json serializable
        json_str_payload = json.dumps(
            mock_client.call_args.kwargs["kwargs"]["standard_logging_object"]
        )
        json.loads(json_str_payload)

        ## response cost
        # Audio streaming responses may not always report token counts,
        # leading to 0.0 cost. Only assert > 0 for non-streaming.
        if not stream:
            assert (
                mock_client.call_args.kwargs["kwargs"]["standard_logging_object"][
                    "response_cost"
                ]
                > 0
            )
        else:
            assert (
                mock_client.call_args.kwargs["kwargs"]["standard_logging_object"][
                    "response_cost"
                ]
                >= 0
            )
        assert (
            mock_client.call_args.kwargs["kwargs"]["standard_logging_object"][
                "model_map_information"
            ]["model_map_value"]
            is not None
        )

        ## turn off message logging
        slobject: StandardLoggingPayload = mock_client.call_args.kwargs["kwargs"][
            "standard_logging_object"
        ]
        if turn_off_message_logging:
            print("checks redacted-by-litellm")
            assert "redacted-by-litellm" == slobject["messages"][0]["content"]
            response = slobject["response"]
            if "choices" in response:
                redacted_content = response["choices"][0]["message"]["content"]
                if stream:
                    assert redacted_content == "redacted-by-litellm"
                else:
                    assert redacted_content is None
                assert response["choices"][0]["message"].get("audio") is None
            else:
                assert response["text"] == "redacted-by-litellm"




@pytest.mark.parametrize(
    "turn_off_message_logging",
    [False, True],
)  # False
def test_logging_async_cache_hit_sync_call(turn_off_message_logging):
    from waypoint.types.utils import StandardLoggingPayload

    waypoint.turn_off_message_logging = turn_off_message_logging

    waypoint.cache = Cache()

    primingHandler = CompletionCustomHandler()
    waypoint.callbacks = [primingHandler]

    response = waypoint.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hey, how's it going?"}],
        caching=True,
        stream=True,
    )
    for chunk in response:
        print(chunk)

    wait_until(
        lambda: "sync_success" in primingHandler.states,
        message=f"priming call never finished logging, states={primingHandler.states}",
    )
    customHandler = CompletionCustomHandler()
    waypoint.callbacks = [customHandler]
    waypoint.success_callback = []

    with patch.object(
        customHandler, "log_success_event", new=MagicMock()
    ) as mock_client:
        resp = waypoint.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hey, how's it going?"}],
            caching=True,
            stream=True,
        )

        for chunk in resp:
            print(chunk)

        wait_until(lambda: mock_client.called, message="log_success_event never fired")
        mock_client.assert_called_once()

        assert "standard_logging_object" in mock_client.call_args.kwargs["kwargs"]
        assert (
            mock_client.call_args.kwargs["kwargs"]["standard_logging_object"]
            is not None
        )

        standard_logging_object: StandardLoggingPayload = mock_client.call_args.kwargs[
            "kwargs"
        ]["standard_logging_object"]

        assert standard_logging_object["cache_hit"] is True
        assert standard_logging_object["response_cost"] == 0
        assert standard_logging_object["saved_cache_cost"] > 0

        if turn_off_message_logging:
            print("checks redacted-by-litellm")
            assert (
                "redacted-by-litellm"
                == standard_logging_object["messages"][0]["content"]
            )
            # response is a full ModelResponse dict (choices format) since d84e5e381acf
            assert (
                standard_logging_object["response"]["choices"][0]["message"]["content"]
                == "redacted-by-litellm"
            )


def test_logging_standard_payload_failure_call():
    from waypoint.types.utils import StandardLoggingPayload

    customHandler = CompletionCustomHandler()
    waypoint.callbacks = [customHandler]

    with patch.object(
        customHandler, "log_failure_event", new=MagicMock()
    ) as mock_client:
        try:
            resp = waypoint.completion(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hey, how's it going?"}],
                api_key="my-bad-api-key",
            )
        except waypoint.AuthenticationError:
            pass

        mock_client.assert_called_once()

        assert "standard_logging_object" in mock_client.call_args.kwargs["kwargs"]
        assert (
            mock_client.call_args.kwargs["kwargs"]["standard_logging_object"]
            is not None
        )

        standard_logging_object: StandardLoggingPayload = mock_client.call_args.kwargs[
            "kwargs"
        ]["standard_logging_object"]
        assert "additional_headers" in standard_logging_object["hidden_params"]


@pytest.mark.parametrize("stream", [False, True])
def test_logging_standard_payload_llm_headers(stream):
    from waypoint.types.utils import StandardLoggingPayload

    # sync completion
    customHandler = CompletionCustomHandler()
    waypoint.callbacks = [customHandler]

    with patch.object(
        customHandler, "log_success_event", new=MagicMock()
    ) as mock_client:

        resp = waypoint.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hey, how's it going?"}],
            stream=stream,
        )

        if stream:
            for chunk in resp:
                continue

        wait_until(lambda: mock_client.called, message="log_success_event never fired")
        mock_client.assert_called()

        standard_logging_object: StandardLoggingPayload = mock_client.call_args.kwargs[
            "kwargs"
        ]["standard_logging_object"]

        print(standard_logging_object["hidden_params"]["additional_headers"])


def test_logging_key_masking_gemini():
    customHandler = CompletionCustomHandler()
    waypoint.callbacks = [customHandler]
    waypoint.success_callback = []

    with patch.object(
        customHandler, "log_pre_api_call", new=MagicMock()
    ) as mock_client:
        try:
            resp = waypoint.completion(
                model="gemini/gemini-1.5-pro",
                messages=[{"role": "user", "content": "Hey, how's it going?"}],
                api_key="LEAVE_ONLY_LAST_4_CHAR_UNMASKED_THIS_PART",
            )
        except waypoint.AuthenticationError:
            pass

        mock_client.assert_called()

        # Gemini API keys are now transmitted via the x-goog-api-key header
        # instead of the legacy ?key=... URL query parameter (security commit
        # 25f93bed91). Verify the key never appears in api_base.
        api_base = mock_client.call_args.kwargs["kwargs"]["litellm_params"]["api_base"]
        assert "LEAVE_ONLY_LAST_4_CHAR_UNMASKED_THIS_PART" not in api_base
        assert "?key=" not in api_base
        assert "&key=" not in api_base


@pytest.mark.parametrize("sync_mode", [True, False])
@pytest.mark.asyncio
async def test_standard_logging_payload_stream_usage(sync_mode):
    """
    Even if stream_options is not provided, correct usage should be logged
    """
    from waypoint.main import stream_chunk_builder
    from waypoint.types.utils import StandardLoggingPayload

    stream = True
    try:
        # sync completion
        customHandler = CompletionCustomHandler()
        waypoint.callbacks = [customHandler]

        if sync_mode:
            patch_event = "log_success_event"
            return_val = MagicMock()
        else:
            patch_event = "async_log_success_event"
            return_val = AsyncMock()

        with patch.object(customHandler, patch_event, new=return_val) as mock_client:
            if sync_mode:
                resp = waypoint.completion(
                    model="anthropic/claude-sonnet-4-5-20250929",
                    messages=[{"role": "user", "content": "Hey, how's it going?"}],
                    stream=stream,
                )

                chunks = []
                for chunk in resp:
                    chunks.append(chunk)
                wait_until(lambda: mock_client.called, message="log_success_event never fired")
            else:
                resp = await waypoint.acompletion(
                    model="anthropic/claude-sonnet-4-5-20250929",
                    messages=[{"role": "user", "content": "Hey, how's it going?"}],
                    stream=stream,
                )

                chunks = []
                async for chunk in resp:
                    chunks.append(chunk)
                await await_until(
                    lambda: mock_client.called, message="async_log_success_event never fired"
                )

            mock_client.assert_called_once()

            standard_logging_object: StandardLoggingPayload = (
                mock_client.call_args.kwargs["kwargs"]["standard_logging_object"]
            )

            built_response = stream_chunk_builder(chunks=chunks)
            print(f"built_response: {built_response}")
            assert (
                built_response.usage.total_tokens
                == standard_logging_object["total_tokens"]
            )
            print(f"standard_logging_object usage: {built_response.usage}")
    except waypoint.InternalServerError:
        pass
