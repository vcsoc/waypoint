from collections.abc import Awaitable, Callable
from datetime import date
from typing import Annotated, Final
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

import waypoint
from waypoint.proxy._types import LitellmUserRoles, UserAPIKeyAuth
from waypoint.proxy.auth.user_api_key_auth import user_api_key_auth
from waypoint.repositories.model_pricing_repository import ModelPricingRepository
from waypoint.types.proxy.user_preferences import validate_timezone
from waypoint.waypoint_core_utils.model_pricing import (
    ModelPricingReport,
    PricingCatalog,
    PricingDeployment,
    model_pricing,
)

router: Final = APIRouter()


class PricingRouter(BaseModel):
    model_config = ConfigDict(frozen=True, from_attributes=True)
    model_list: tuple[PricingDeployment, ...]


class PricingDatabase(BaseModel):
    model_config = ConfigDict(frozen=True, from_attributes=True)
    query_raw: Callable[[str, str, str, str], Awaitable[object]]


@router.get("/model-pricing", tags=["model management"], response_model=ModelPricingReport)
async def get_model_pricing(
    user_api_key_dict: Annotated[UserAPIKeyAuth, Depends(user_api_key_auth)],
    start_date: date | None = None,
    end_date: date | None = None,
    timezone_name: str = "UTC",
) -> ModelPricingReport:
    from waypoint.proxy.proxy_server import llm_router, prisma_client

    if user_api_key_dict.user_role not in (LitellmUserRoles.PROXY_ADMIN, LitellmUserRoles.PROXY_ADMIN_VIEW_ONLY):
        raise HTTPException(status_code=403, detail="Only proxy admins can view deployment-wide pricing estimates")
    if llm_router is None:
        raise HTTPException(status_code=503, detail="Model router is unavailable")
    deployments: Final = PricingRouter.model_validate(llm_router).model_list
    catalog: Final = PricingCatalog.model_validate(vars(waypoint)).model_cost
    if start_date is None and end_date is None:
        return ModelPricingReport(pricing=tuple(model_pricing(entry, catalog) for entry in deployments))
    if start_date is None or end_date is None or start_date > end_date:
        raise HTTPException(status_code=422, detail="A valid start_date and end_date are required")
    try:
        zone: Final = ZoneInfo(validate_timezone(timezone_name))
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid reporting timezone") from None
    if prisma_client is None:
        raise HTTPException(status_code=503, detail="Database is unavailable")
    query: Final = PricingDatabase.model_validate(prisma_client.db).query_raw
    return await ModelPricingRepository(query).report(
        deployments=deployments, catalog=catalog, start=start_date, end=end_date, zone=zone,
    )
