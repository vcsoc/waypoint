"""
Waypoint agent tracing: OTLP traces from agents, joined to Waypoint spend logs, in ClickHouse.

"""

from waypoint.rust_bridge.trace.storage import Tenant
from waypoint.tracing.otlp_http import TracingPayloadTooLargeError
from waypoint.tracing.receiver import TraceReceiver

__all__ = (
    "Tenant",
    "TraceReceiver",
    "TracingPayloadTooLargeError",
)
