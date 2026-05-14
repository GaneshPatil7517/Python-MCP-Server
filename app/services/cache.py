"""
Caching service for application-level caching.
Supports in-memory and Redis-based caching.
"""

import json
import logging
from typing import Optional, Any, Dict
from datetime import datetime, timedelta
import hashlib


logger = logging.getLogger("app")


class CacheService:
    """Base cache service."""
    
    async def get(self, key: str) -> Optional[Any]:
        raise NotImplementedError
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        raise NotImplementedError
    
    async def delete(self, key: str) -> bool:
        raise NotImplementedError
    
    async def clear(self) -> bool:
        raise NotImplementedError


class InMemoryCacheService(CacheService):
    """Simple in-memory cache implementation."""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        if entry["expires_at"] < datetime.utcnow():
            del self._cache[key]
            return None
        
        entry["hits"] += 1
        return entry["value"]
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache."""
        self._cache[key] = {
            "value": value,
            "expires_at": datetime.utcnow() + timedelta(seconds=ttl),
            "hits": 0,
        }
        return True
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    async def clear(self) -> bool:
        """Clear all cache entries."""
        self._cache.clear()
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        now = datetime.utcnow()
        active_entries = sum(
            1 for entry in self._cache.values()
            if entry["expires_at"] > now
        )
        total_hits = sum(entry["hits"] for entry in self._cache.values())
        
        return {
            "total_entries": len(self._cache),
            "active_entries": active_entries,
            "total_hits": total_hits,
        }


class RedisCacheService(CacheService):
    """Redis-based cache implementation."""
    
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self._client = None
    
    async def connect(self):
        """Connect to Redis."""
        try:
            import redis.asyncio
            self._client = redis.asyncio.from_url(self.redis_url)
            await self._client.ping()
            logger.info("Connected to Redis cache")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            raise
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self._client:
            await self._client.close()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache."""
        if not self._client:
            return None
        
        try:
            value = await self._client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis get error: {str(e)}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in Redis cache."""
        if not self._client:
            return False
        
        try:
            await self._client.setex(
                key,
                ttl,
                json.dumps(value, default=str),
            )
            return True
        except Exception as e:
            logger.error(f"Redis set error: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from Redis cache."""
        if not self._client:
            return False
        
        try:
            result = await self._client.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"Redis delete error: {str(e)}")
            return False
    
    async def clear(self) -> bool:
        """Clear all Redis cache entries."""
        if not self._client:
            return False
        
        try:
            await self._client.flushdb()
            return True
        except Exception as e:
            logger.error(f"Redis clear error: {str(e)}")
            return False


def generate_cache_key(*parts: str, **kwargs) -> str:
    """Generate cache key from parts and kwargs."""
    key_parts = list(parts) + [f"{k}:{v}" for k, v in sorted(kwargs.items())]
    key_string = ":".join(str(p) for p in key_parts)
    return hashlib.sha256(key_string.encode()).hexdigest()[:32]
