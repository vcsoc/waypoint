from typing import Final

import pytest
from fastapi import HTTPException

from waypoint.proxy._types import LitellmUserRoles, UserAPIKeyAuth
from waypoint.proxy.management_endpoints.model_pricing_endpoints import get_model_pricing


@pytest.mark.asyncio
async def test_regular_keys_cannot_read_deployment_wide_pricing_history() -> None:
    auth: Final = UserAPIKeyAuth(user_role=LitellmUserRoles.INTERNAL_USER)
    with pytest.raises(HTTPException) as error:
        await get_model_pricing(auth)
    assert error.value.status_code == 403
