import asyncio
from typing import Final

import httpx
import pytest
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route, Router

from waypoint.proxy.middleware.custom_license_refresh_middleware import CustomLicenseRefreshMiddleware


class LicensePolicy:
    def __init__(self) -> None:
        self.time = 0.0
        self.premium = True
        self.applied = False
        self.checks = 0

    def check(self) -> bool:
        self.checks += 1
        return self.premium

    def apply(self, verdict: bool) -> None:
        self.applied = verdict

    def clock(self) -> float:
        return self.time

    async def endpoint(self, request: Request) -> Response:
        return Response(status_code=200 if self.applied else 403)


@pytest.mark.asyncio
async def test_premium_gate_refreshes_after_ttl_and_serializes_concurrent_requests() -> None:
    policy: Final = LicensePolicy()
    app: Final = CustomLicenseRefreshMiddleware(
        Router(routes=[Route("/enterprise", policy.endpoint)]),
        check=policy.check,
        apply=policy.apply,
        clock=policy.clock,
    )
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app), base_url="http://test") as client:
        assert (await client.get("/enterprise")).status_code == 200
        policy.premium = False
        assert (await client.get("/enterprise")).status_code == 200
        policy.time = 30.0
        assert (await client.get("/enterprise")).status_code == 403
        policy.premium = True
        assert (await client.get("/enterprise")).status_code == 403
        policy.time = 60.0
        results: Final = await asyncio.gather(*(client.get("/enterprise") for _ in range(8)))
        assert all(result.status_code == 200 for result in results)
        assert policy.checks == 3
