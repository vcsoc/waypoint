from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Final
from zoneinfo import ZoneInfo

from waypoint.proxy.route_llm_request import ROUTE_ENDPOINT_MAPPING
from waypoint.repositories.daily_activity_sql import PRISMA_TO_PG_TABLE, SqlQuery
from waypoint.types.repositories.daily_activity import DailyActivityScope, DailyActivityTable


@dataclass(frozen=True, slots=True)
class LocalDayWindow:
    start: datetime
    end: datetime


def local_day_window(start: date, end: date, zone: ZoneInfo) -> LocalDayWindow:
    return LocalDayWindow(
        datetime.combine(start, time.min, zone).astimezone(timezone.utc),
        datetime.combine(end + timedelta(days=1), time.min, zone).astimezone(timezone.utc),
    )


def _number(path: str, *, integer: bool = True) -> str:
    cast: Final = "::bigint" if integer else ""
    return (
        f"CASE WHEN jsonb_typeof(l.metadata #> '{{{path}}}') = 'number' "
        f"THEN (l.metadata #>> '{{{path}}}')::numeric{cast} ELSE 0 END"
    )


def _first_number(paths: tuple[str, ...]) -> str:
    return "COALESCE(" + ", ".join(f"NULLIF(({_number(path)}), 0)" for path in paths) + ", 0)"


def localize_daily_query(scope: DailyActivityScope, query: SqlQuery) -> SqlQuery:
    if scope.timezone_name is None or scope.timezone_name == "UTC":
        return query
    zone: Final = ZoneInfo(scope.timezone_name)
    window: Final = local_day_window(date.fromisoformat(scope.start_date), date.fromisoformat(scope.end_date), zone)
    zone_param: Final = len(query.params) + 1
    start_param: Final = zone_param + 1
    end_param: Final = zone_param + 2
    pg_table: Final = PRISMA_TO_PG_TABLE[scope.table]
    source_sql: Final = query.sql.replace(f'"{pg_table}"', '"local_daily"')
    tag_join: Final = (
        "CROSS JOIN LATERAL (SELECT DISTINCT value AS tag FROM jsonb_array_elements_text("
        "CASE WHEN jsonb_typeof(l.request_tags) = 'array' THEN l.request_tags ELSE '[]'::jsonb END)) tags"
        if scope.table is DailyActivityTable.TAG else ""
    )
    tag_select: Final = "tags.tag" if scope.table is DailyActivityTable.TAG else "NULL::text"
    cache_read: Final = _first_number((
        "usage_object,cache_read_input_tokens", "usage_object,prompt_tokens_details,cached_tokens",
    ))
    cache_write: Final = _first_number((
        "usage_object,cache_creation_input_tokens", "usage_object,prompt_tokens_details,cache_write_tokens",
        "usage_object,prompt_tokens_details,cache_creation_tokens",
    ))
    endpoint_cases: Final = " ".join(f"WHEN '{kind}' THEN '{path}'" for kind, path in ROUTE_ENDPOINT_MAPPING.items())
    internal: Final = "COALESCE(l.metadata->>'internal_call_origin', '') <> ''"
    success: Final = "COALESCE(l.status, 'success') = 'success'"
    timed: Final = f"NOT ({internal}) AND ({success}) AND l.request_duration_ms >= 0"
    sql: Final = f'''WITH local_daily AS (
        SELECT to_char(timezone(${zone_param}, l."startTime" AT TIME ZONE 'UTC'), 'YYYY-MM-DD') AS date,
               l.api_key, l.model, l.model_group, l.custom_llm_provider, l.mcp_namespaced_tool_name,
               CASE l.call_type {endpoint_cases} ELSE NULL END AS endpoint,
               l."user" AS user_id, l.team_id, l.organization_id, l.end_user AS end_user_id,
               l.agent_id, {tag_select} AS tag,
               l.spend, 0::float AS ptu_flat_cost, l.prompt_tokens, l.completion_tokens,
               {cache_read} AS cache_read_input_tokens, {cache_write} AS cache_creation_input_tokens,
               {_number('compression_savings,tokens_saved')} AS compression_saved_tokens,
               {_number('compression_savings_spend', integer=False)}::float AS compression_savings_spend,
               {_number('prompt_caching_savings_spend', integer=False)}::float AS prompt_caching_savings_spend,
               {_number('gateway_injected_caching_savings_spend', integer=False)}::float AS gateway_injected_caching_savings_spend,
               {_number('autorouter_savings_spend', integer=False)}::float AS autorouter_savings_spend,
               CASE WHEN {internal} THEN 0 ELSE 1 END AS api_requests,
               CASE WHEN NOT ({internal}) AND ({success}) THEN 1 ELSE 0 END AS successful_requests,
               CASE WHEN NOT ({internal}) AND NOT ({success}) THEN 1 ELSE 0 END AS failed_requests,
               CASE WHEN {timed} THEN l.request_duration_ms ELSE 0 END AS total_response_time_ms,
               CASE WHEN {timed} THEN 1 ELSE 0 END AS timed_requests
        FROM "LiteLLM_SpendLogs" l {tag_join}
        WHERE l."startTime" >= ${start_param}::timestamp AND l."startTime" < ${end_param}::timestamp
    ) SELECT * FROM ({source_sql}) localized_result'''
    return SqlQuery(sql, (*query.params, scope.timezone_name,
        window.start.replace(tzinfo=None), window.end.replace(tzinfo=None)))
