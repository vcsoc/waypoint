from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

import pytest

from waypoint.waypoint_core_utils.model_pricing import (
    PricingDeployment,
    PricingParams,
    PricingUsage,
    estimate_value,
    model_pricing,
    with_model_pricing,
)

_RATE: Final = MappingProxyType({
    "input_cost_per_token": 0.000003,
    "output_cost_per_token": 0.000012,
    "cache_read_input_token_cost": 0.000001,
    "input_cost_per_token_above_1k_tokens": 0.000006,
    "output_cost_per_token_above_1k_tokens": 0.000024,
    "cache_read_input_token_cost_above_1k_tokens": 0.000002,
    "source": "https://example.test/pricing",
})


@pytest.mark.parametrize(("model", "reference", "basis"), (
    ("chatgpt/test-model", "test-model", "published_api_rate"),
    ("ollama_chat/qwen3.5:2b", "openrouter/qwen/qwen3.5-9b", "hosted_qwen_benchmark"),
    ("ollama_chat/qwen3.5:4b", "openrouter/qwen/qwen3.5-9b", "hosted_qwen_benchmark"),
    ("ollama/gemma3:4b", "openrouter/google/gemma-3-4b-it", "hosted_model_equivalent"),
))
def test_configured_models_resolve_to_labeled_catalog_pricing(model: str, reference: str, basis: str) -> None:
    quote: Final = model_pricing(PricingDeployment(model_name="alias", litellm_params=PricingParams(model=model)),
                                {reference: _RATE})
    assert quote.model_name == "alias"
    assert quote.catalog_model == reference
    assert quote.basis == basis
    assert quote.source == _RATE["source"]
    assert quote.tiers[0].input_per_token == _RATE["input_cost_per_token"]
    assert quote.tiers[0].output_per_token == _RATE["output_cost_per_token"]


@pytest.mark.parametrize("prompt", (1000, 1001))
def test_estimates_apply_per_request_context_tiers_and_cached_input(prompt: int) -> None:
    quote: Final = model_pricing(PricingDeployment(model_name="alias", litellm_params=PricingParams(model="test")),
                                {"test": _RATE})
    usage: Final = PricingUsage(date="2026-01-01", model_name="alias", model="test", prompt_tokens=prompt,
                               completion_tokens=25, cached_tokens=100, requests=7)
    result: Final = estimate_value(usage, quote)
    tier: Final = quote.tiers[0 if prompt == 1000 else 1]
    assert result.estimated_cost == pytest.approx(usage.requests * (
        (prompt - usage.cached_tokens) * tier.input_per_token
        + usage.cached_tokens * tier.cached_input_per_token + usage.completion_tokens * tier.output_per_token
    ))
    assert result.estimated_requests == usage.requests
    assert result.missing_rate_requests == 0


def test_cached_tokens_cannot_create_negative_input_cost() -> None:
    quote: Final = model_pricing(PricingDeployment(model_name="alias", litellm_params=PricingParams(model="test")),
                                {"test": _RATE})
    usage: Final = PricingUsage(date="2026-01-01", model_name="alias", model="test", prompt_tokens=10,
                               completion_tokens=0, cached_tokens=100, requests=1)
    result: Final = estimate_value(usage, quote)
    assert result.estimated_cost == pytest.approx(usage.prompt_tokens * quote.tiers[0].cached_input_per_token)


@pytest.mark.parametrize("invalid", (None, True, -1, float("nan"), float("inf")))
def test_missing_or_invalid_pricing_is_unknown_not_free(invalid: object) -> None:
    quote: Final = model_pricing(PricingDeployment(model_name="alias", litellm_params=PricingParams(model="test")),
                                {"test": {**_RATE, "input_cost_per_token": invalid}})
    usage: Final = PricingUsage(date="2026-01-01", model_name="alias", model="test", prompt_tokens=10,
                               completion_tokens=1, requests=3, cached_tokens=0)
    result: Final = estimate_value(usage, quote)
    assert quote.basis == "unavailable"
    assert result.estimated_cost is None
    assert result.missing_rate_requests == usage.requests


def test_enrichment_preserves_actual_rates_and_does_not_mutate_config() -> None:
    info: Final = MappingProxyType({"input_cost_per_token": 0, "output_cost_per_token": 0, "id": "deployment"})
    deployment: Final = MappingProxyType({
        "model_name": "alias", "litellm_params": {"model": "chatgpt/test", "api_key": "private-fixture"},
        "model_info": info,
    })
    enriched: Final = with_model_pricing(deployment, {"test": _RATE})
    enriched_info: Final = enriched["model_info"]
    assert isinstance(enriched_info, Mapping)
    assert enriched_info["input_cost_per_token"] == info["input_cost_per_token"]
    assert enriched_info["output_cost_per_token"] == info["output_cost_per_token"]
    assert "api_equivalent_pricing" in enriched_info
    assert "api_equivalent_pricing" not in info
    assert enriched["litellm_params"] == deployment["litellm_params"]
