"""waypoint.sandbox: code-interpreter providers (see main.py) plus harness sandboxes.

`sandbox.local(path)` and `sandbox.docker(image, ...)` re-export waypoint.harness.sandbox.
They resolve lazily so `import waypoint` does not pull in waypoint.harness.
"""

import importlib
from typing import Final

_HARNESS_SANDBOX_MODULE: Final = "waypoint.harness.sandbox"
_HARNESS_EXPORTS: Final = frozenset(
    {
        "local",
        "docker",
        "LocalSandbox",
        "DockerSandbox",
        "Sandbox",
        "Process",
        "CompletedRun",
    }
)


def __getattr__(name: str) -> object:
    if name in _HARNESS_EXPORTS:
        return getattr(importlib.import_module(_HARNESS_SANDBOX_MODULE), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
