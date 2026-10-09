import asyncio
import time
from collections.abc import Callable
from typing import Final

from starlette.types import ASGIApp, Receive, Scope, Send

from waypoint.proxy._types import EnterpriseLicenseData


class CustomLicenseRefreshMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        check: Callable[[], bool],
        apply: Callable[[bool], None],
        interval: float = 30,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.app = app
        self.check = check
        self.apply = apply
        self.interval = interval
        self.clock = clock
        self.last_checked = float("-inf")
        self.lock = asyncio.Lock()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in {"http", "websocket"}:
            async with self.lock:
                if self.clock() - self.last_checked >= self.interval:
                    verdict: Final = await asyncio.to_thread(self.check)
                    self.apply(verdict)
                    self.last_checked = self.clock()
        await self.app(scope, receive, send)


def apply_custom_license_verdict(verdict: bool, data: EnterpriseLicenseData | None) -> None:
    from waypoint.proxy import proxy_server

    proxy_server.premium_user = verdict
    proxy_server.premium_user_data = data if verdict else None
