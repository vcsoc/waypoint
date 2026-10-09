"""Single source of truth for whether ``waypoint.request_timeout`` was configured.

``waypoint.request_timeout`` always holds a value (the package default,
:data:`~waypoint.constants.DEFAULT_REQUEST_TIMEOUT_SECONDS`), so a bare read can't
tell "user asked for this" from "nobody set it". This resolver answers that:

* ``request_timeout_explicitly_set`` is the authoritative signal, set when the
  value comes from the ``REQUEST_TIMEOUT`` env var or ``litellm_settings``.
* A runtime value that differs from the package default (e.g. ``waypoint.request_timeout
  = 300`` in SDK code) is also treated as explicit, for backwards compatibility.
"""

from __future__ import annotations

from typing import Final

from waypoint.constants import DEFAULT_REQUEST_TIMEOUT_SECONDS


def get_configured_request_timeout() -> float | None:
    """Return the explicitly-configured ``waypoint.request_timeout``, else ``None``."""
    import waypoint

    timeout: Final = float(waypoint.request_timeout)
    if waypoint.request_timeout_explicitly_set:
        return timeout
    if timeout != float(DEFAULT_REQUEST_TIMEOUT_SECONDS):
        return timeout
    return None
