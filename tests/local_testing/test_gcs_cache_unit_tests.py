from cache_unit_tests import LLMCachingUnitTests
from waypoint.caching import LiteLLMCacheType


class TestGCSCacheUnitTests(LLMCachingUnitTests):
    def get_cache_type(self) -> LiteLLMCacheType:
        return LiteLLMCacheType.GCS
