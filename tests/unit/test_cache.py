"""
Unit tests for services.
"""

import pytest
from app.services.cache import InMemoryCacheService, generate_cache_key


@pytest.mark.asyncio
async def test_in_memory_cache():
    """Test in-memory cache service."""
    cache = InMemoryCacheService()

    # Test set and get
    await cache.set("test_key", {"data": "test_value"}, ttl=3600)
    result = await cache.get("test_key")

    assert result == {"data": "test_value"}

    # Test delete
    deleted = await cache.delete("test_key")
    assert deleted is True

    result = await cache.get("test_key")
    assert result is None


@pytest.mark.asyncio
async def test_cache_expiration():
    """Test cache expiration."""
    import asyncio

    cache = InMemoryCacheService()

    # Set with short TTL
    await cache.set("expiring_key", "value", ttl=1)

    # Should exist initially
    result = await cache.get("expiring_key")
    assert result == "value"

    # Wait for expiration
    await asyncio.sleep(1.1)

    # Should be expired
    result = await cache.get("expiring_key")
    assert result is None


def test_cache_key_generation():
    """Test cache key generation."""
    key1 = generate_cache_key("tool", "weather", "city", city="London")
    key2 = generate_cache_key("tool", "weather", "city", city="London")
    key3 = generate_cache_key("tool", "weather", "city", city="Paris")

    assert key1 == key2
    assert key1 != key3
    assert len(key1) == 32  # SHA256 truncated to 32 chars
