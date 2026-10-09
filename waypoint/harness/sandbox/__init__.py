"""Sandboxes for waypoint.harness: where the runtime runs and which files it can touch."""

from waypoint.harness.sandbox.base import CompletedRun, Process, Sandbox
from waypoint.harness.sandbox.docker import DockerSandbox, docker
from waypoint.harness.sandbox.local import LocalSandbox, local
from waypoint.harness.sandbox.snapshot import (
    build_file_changes,
    capture_text_contents,
    diff_snapshots,
    snapshot_local,
)

__all__ = (
    "CompletedRun",
    "DockerSandbox",
    "LocalSandbox",
    "Process",
    "Sandbox",
    "build_file_changes",
    "capture_text_contents",
    "diff_snapshots",
    "docker",
    "local",
    "snapshot_local",
)
