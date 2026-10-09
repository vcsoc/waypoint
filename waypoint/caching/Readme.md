# Caching on Waypoint

Waypoint supports multiple caching mechanisms. This allows users to choose the most suitable caching solution for their use case.

The following caching mechanisms are supported:

1. **RedisCache**
2. **RedisSemanticCache**
3. **QdrantSemanticCache**
4. **InMemoryCache**
5. **DiskCache**
6. **S3Cache**
7. **AzureBlobCache**
8. **DualCache** (updates both Redis and an in-memory cache simultaneously)

## Folder Structure

```
waypoint/caching/
├── base_cache.py
├── caching.py
├── caching_handler.py
├── disk_cache.py
├── dual_cache.py
├── in_memory_cache.py
├── qdrant_semantic_cache.py
├── redis_cache.py
├── redis_semantic_cache.py
├── s3_cache.py
```

## Documentation
- [Caching on Waypoint Gateway](https://docs.litellm.ai/docs/proxy/caching)
- [Caching on Waypoint Python](https://docs.litellm.ai/docs/caching/all_caches)







