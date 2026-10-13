from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from datetime import date
from types import MappingProxyType
from typing import Final
from zoneinfo import ZoneInfo

from pydantic import TypeAdapter

from waypoint.repositories.daily_activity_timezone import cache_read_tokens_sql, local_day_window
from waypoint.waypoint_core_utils.model_pricing import (
    ModelPricingReport,
    PricingDeployment,
    PricingParams,
    PricingUsage,
    estimate_value,
    model_pricing,
)

_USAGE: Final = TypeAdapter(tuple[PricingUsage, ...])
_QUERY: Final = f'''SELECT to_char(timezone($3, l."startTime" AT TIME ZONE 'UTC'), 'YYYY-MM-DD') AS date,
    COALESCE(NULLIF(l.model_group, ''), l.model, '') AS model_name,
    COALESCE(l.model, '') AS model,
    GREATEST(l.prompt_tokens, 0) AS prompt_tokens,
    GREATEST(l.completion_tokens, 0) AS completion_tokens,
    GREATEST(({cache_read_tokens_sql()})::bigint, 0) AS cached_tokens,
    COUNT(*)::bigint AS requests
    FROM "LiteLLM_SpendLogs" l
    WHERE l."startTime" >= $1::timestamp AND l."startTime" < $2::timestamp
      AND COALESCE(l.status, 'success') = 'success'
      AND LOWER(COALESCE(l.cache_hit, '')) NOT IN ('true', '1')
      AND COALESCE(l.metadata->>'internal_call_origin', '') = ''
    GROUP BY 1, 2, 3, 4, 5, 6 ORDER BY 1, 2, 3, 4, 5, 6'''


@dataclass(frozen=True, slots=True)
class ModelPricingRepository:
    query: Callable[[str, str, str, str], Awaitable[object]]

    async def report(
        self, *, deployments: tuple[PricingDeployment, ...], catalog: Mapping[str, Mapping[str, object]],
        start: date, end: date, zone: ZoneInfo,
    ) -> ModelPricingReport:
        window: Final = local_day_window(start, end, zone)
        rows: Final = _USAGE.validate_python(await self.query(
            _QUERY, window.start.isoformat(), window.end.isoformat(), zone.key,
        ))
        by_name: Final = MappingProxyType({entry.model_name: entry for entry in deployments})
        daily: Final = tuple(
            estimate_value(row, model_pricing(by_name.get(row.model_name) or PricingDeployment(
                model_name=row.model_name, litellm_params=PricingParams(model=row.model),
            ), catalog)) for row in rows
        )
        estimated_requests: Final = sum(row.estimated_requests for row in daily)
        return ModelPricingReport(
            pricing=tuple(model_pricing(deployment, catalog) for deployment in deployments), daily=daily,
            estimated_cost=sum(row.estimated_cost or 0 for row in daily) if estimated_requests else None,
            estimated_requests=estimated_requests, missing_rate_requests=sum(row.missing_rate_requests for row in daily),
        )
