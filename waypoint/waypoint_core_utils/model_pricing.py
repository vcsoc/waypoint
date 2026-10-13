from __future__ import annotations

import math
import re
from collections.abc import Mapping
from functools import cache
from types import MappingProxyType
from typing import Final, Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, JsonValue, TypeAdapter

from waypoint.waypoint_core_utils.get_model_cost_map import GetModelCostMap

_LOCAL_REFERENCES: Final = MappingProxyType({
    "qwen3.5:2b": "openrouter/qwen/qwen3.5-9b",
    "qwen3.5:4b": "openrouter/qwen/qwen3.5-9b",
    "gemma3:4b": "openrouter/google/gemma-3-4b-it",
})
_JSON_MAPPING: Final = TypeAdapter(Mapping[str, JsonValue])
_INFO_MAPPING: Final = TypeAdapter(Mapping[str, object])
_THRESHOLD: Final = re.compile(r"^input_cost_per_token_above_(\d+)(k|m)?_tokens$")


class PricingCatalog(BaseModel):
    model_config = ConfigDict(frozen=True, from_attributes=True)
    model_cost: Mapping[str, Mapping[str, object]] = Field(validation_alias=AliasChoices("model_cost", "model_cost_map"))


class PricingParams(BaseModel):
    model_config = ConfigDict(frozen=True)
    model: str


class PricingDeployment(BaseModel):
    model_config = ConfigDict(frozen=True)
    model_name: str
    litellm_params: PricingParams


class PricingTier(BaseModel):
    model_config = ConfigDict(frozen=True)
    above_tokens: int = 0
    input_per_token: float = Field(ge=0)
    output_per_token: float = Field(ge=0)
    cached_input_per_token: float = Field(ge=0)


class ModelPricing(BaseModel):
    model_config = ConfigDict(frozen=True)
    model_name: str
    catalog_model: str
    basis: Literal["published_api_rate", "hosted_model_equivalent", "hosted_qwen_benchmark", "unavailable"]
    currency: Literal["USD"] = "USD"
    source: str | None
    tiers: tuple[PricingTier, ...]


class PricingUsage(BaseModel):
    model_config = ConfigDict(frozen=True)
    date: str
    model_name: str
    model: str
    prompt_tokens: int = Field(ge=0)
    completion_tokens: int = Field(ge=0)
    cached_tokens: int = Field(ge=0)
    requests: int = Field(ge=0)


class ModelValue(BaseModel):
    model_config = ConfigDict(frozen=True)
    date: str
    model_name: str
    estimated_cost: float | None
    estimated_requests: int
    missing_rate_requests: int


class ModelPricingReport(BaseModel):
    model_config = ConfigDict(frozen=True)
    pricing: tuple[ModelPricing, ...]
    daily: tuple[ModelValue, ...] = ()
    estimated_cost: float | None = None
    estimated_requests: int = 0
    missing_rate_requests: int = 0
    currency: Literal["USD"] = "USD"


def rate(record: Mapping[str, object], key: str) -> float | None:
    value: Final = record.get(key)
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        return None
    return float(value) if math.isfinite(value) and value >= 0 else None


def _tier_rate(record: Mapping[str, object], key: str, suffix: str) -> float | None:
    specific: Final = rate(record, f"{key}{suffix}")
    return specific if specific is not None else rate(record, key)


def _tier(record: Mapping[str, object], above: int = 0, suffix: str = "") -> PricingTier | None:
    input_rate: Final = rate(record, f"input_cost_per_token{suffix}")
    output_rate: Final = _tier_rate(record, "output_cost_per_token", suffix)
    if input_rate is None or output_rate is None:
        return None
    cached_rate: Final = _tier_rate(record, "cache_read_input_token_cost", suffix)
    return PricingTier(
        above_tokens=above, input_per_token=input_rate, output_per_token=output_rate,
        cached_input_per_token=cached_rate if cached_rate is not None else input_rate,
    )


@cache
def bundled_reference_rates() -> Mapping[str, Mapping[str, object]]:
    bundled: Final = PricingCatalog.model_validate(GetModelCostMap.load_local_model_cost_map_with_revision()).model_cost
    return MappingProxyType({key: bundled[key] for key in frozenset(_LOCAL_REFERENCES.values()) if key in bundled})


def model_pricing(deployment: PricingDeployment, catalog: Mapping[str, Mapping[str, object]]) -> ModelPricing:
    model: Final = deployment.litellm_params.model
    local_model: Final = model.removeprefix("ollama_chat/").removeprefix("ollama/")
    reference: Final = _LOCAL_REFERENCES.get(local_model)
    candidate: Final = reference or model.removeprefix("chatgpt/")
    catalog_model: Final = candidate if reference or candidate in catalog else candidate.partition("/")[2] or candidate
    record: Final = catalog[catalog_model] if catalog_model in catalog else bundled_reference_rates().get(catalog_model, {})
    standard: Final = _tier(record)
    higher: Final = tuple(
        (int(match[1]) * {None: 1, "k": 1000, "m": 1000000}[match[2]], key.removeprefix("input_cost_per_token"))
        for key in record if (match := _THRESHOLD.fullmatch(key)) is not None
    )
    tiers: Final = tuple(tier for above, suffix in higher if (tier := _tier(record, above, suffix)) is not None)
    source: Final = record.get("source")
    return ModelPricing(
        model_name=deployment.model_name, catalog_model=catalog_model,
        basis=("unavailable" if standard is None else "hosted_qwen_benchmark" if reference and local_model.startswith("qwen")
               else "hosted_model_equivalent" if reference else "published_api_rate"),
        source=source if isinstance(source, str) else None,
        tiers=tuple(sorted((standard,) + tiers, key=lambda tier: tier.above_tokens)) if standard else (),
    )


def estimate_value(usage: PricingUsage, pricing: ModelPricing) -> ModelValue:
    applicable: Final = tuple(tier for tier in pricing.tiers if tier.above_tokens == 0 or usage.prompt_tokens > tier.above_tokens)
    if not applicable:
        return ModelValue(date=usage.date, model_name=usage.model_name, estimated_cost=None,
                          estimated_requests=0, missing_rate_requests=usage.requests)
    tier: Final = max(applicable, key=lambda entry: entry.above_tokens)
    cached: Final = min(usage.cached_tokens, usage.prompt_tokens)
    return ModelValue(
        date=usage.date, model_name=usage.model_name,
        estimated_cost=usage.requests * ((usage.prompt_tokens - cached) * tier.input_per_token
                                        + cached * tier.cached_input_per_token
                                        + usage.completion_tokens * tier.output_per_token),
        estimated_requests=usage.requests, missing_rate_requests=0,
    )


def with_model_pricing(deployment: Mapping[str, object], catalog: Mapping[str, Mapping[str, object]]) -> Mapping[str, object]:
    entry: Final = PricingDeployment.model_validate(deployment)
    info: Final = _INFO_MAPPING.validate_python(deployment.get("model_info") or {})
    quote: Final = _JSON_MAPPING.validate_python(model_pricing(entry, catalog).model_dump(mode="json"))
    return {**deployment, "model_info": {**info, "api_equivalent_pricing": quote}}
