import importlib_metadata

try:
    version = importlib_metadata.version("waypoint")
except Exception:
    version = "unknown"
