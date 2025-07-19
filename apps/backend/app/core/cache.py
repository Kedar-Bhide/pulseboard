from functools import wraps
from typing import Any, Callable, Optional
import json
from redis import Redis
from app.core.config import settings

class Cache:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.default_ttl = 300  # 5 minutes

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        self.redis.setex(
            key,
            ttl or self.default_ttl,
            json.dumps(value)
        )

    def delete(self, key: str) -> None:
        """Delete value from cache"""
        self.redis.delete(key)

    def clear_pattern(self, pattern: str) -> None:
        """Clear all keys matching pattern"""
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)

# Global cache instance
_global_cache: Optional[Cache] = None

def get_cache() -> Cache:
    """Get the global cache instance"""
    global _global_cache
    if _global_cache is None:
        import redis
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD or None,
            decode_responses=True
        )
        _global_cache = Cache(redis_client)
    return _global_cache

def cache_response(ttl: Optional[int] = None):
    """Decorator to cache function responses"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cache = get_cache()
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Get fresh value
            value = await func(*args, **kwargs)
            
            # Cache the value
            cache.set(cache_key, value, ttl)
            return value
        return wrapper
    return decorator 