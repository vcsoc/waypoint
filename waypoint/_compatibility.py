import importlib
import importlib.abc
import importlib.util
import sys
from collections.abc import Sequence
from importlib.machinery import ModuleSpec
from types import MappingProxyType, ModuleType
from typing import Final

_MODULE_COMPONENTS: Final = MappingProxyType(
    {
        "litellm": "waypoint",
        "litellm_core_utils": "waypoint_core_utils",
        "litellm_logging": "waypoint_logging",
        "litellm_completion_bridge": "waypoint_completion_bridge",
        "litellm_responses_transformation": "waypoint_responses_transformation",
        "litellm_agent": "waypoint_agent",
        "litellm_agent_model_resolver": "waypoint_agent_model_resolver",
        "get_litellm_params": "get_waypoint_params",
        "litellm_db_storage_backend": "waypoint_db_storage_backend",
        "litellm_proxy": "waypoint_proxy",
        "litellm_auth_handler": "waypoint_auth_handler",
        "litellm_license": "waypoint_license",
        "litellm_executed_batches": "waypoint_executed_batches",
        "litellm_content_filter": "waypoint_content_filter",
        "litellm_skills": "waypoint_skills",
        "litellm_pre_call_utils": "waypoint_pre_call_utils",
        "litellm_completion_transformation": "waypoint_completion_transformation",
        "litellm_proxy_mcp_handler": "waypoint_proxy_mcp_handler",
        "litellm_encoder": "waypoint_encoder",
        "litellm_params": "waypoint_params",
    }
)


class LegacyModuleLoader(importlib.abc.Loader):
    def create_module(self, spec: ModuleSpec) -> ModuleType:
        canonical: Final = ".".join(_MODULE_COMPONENTS.get(part, part) for part in spec.name.split("."))
        return importlib.import_module(canonical)

    def exec_module(self, module: ModuleType) -> None:
        return None


class LegacyModuleFinder(importlib.abc.MetaPathFinder):
    def find_spec(
        self, fullname: str, path: Sequence[str] | None = None, target: ModuleType | None = None
    ) -> ModuleSpec | None:
        if not fullname.startswith(("litellm.", "waypoint.")):
            return None
        canonical: Final = ".".join(_MODULE_COMPONENTS.get(part, part) for part in fullname.split("."))
        if canonical == fullname:
            return None
        canonical_spec: Final = importlib.util.find_spec(canonical)
        if canonical_spec is None:
            return None
        return importlib.util.spec_from_loader(
            fullname, LegacyModuleLoader(), is_package=canonical_spec.submodule_search_locations is not None
        )


def install_legacy_import_aliases() -> None:
    sys.modules.setdefault("litellm", sys.modules["waypoint"])
    if not any(isinstance(finder, LegacyModuleFinder) for finder in sys.meta_path):
        sys.meta_path.insert(0, LegacyModuleFinder())
