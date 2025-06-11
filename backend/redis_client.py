import os

import redis.asyncio as redis

_REDIS: redis.Redis | None = None


def get_redis_url() -> str:
    # Use env var if provided, else default to local docker-compose service name.
    return os.getenv("REDIS_URL", "redis://redis:6379/0")


async def get_redis() -> redis.Redis:
    """Return a singleton async Redis client."""
    global _REDIS
    if _REDIS is None:
        _REDIS = redis.Redis.from_url(get_redis_url(), decode_responses=True)
    return _REDIS


async def close_redis() -> None:
    global _REDIS
    if _REDIS is not None:
        await _REDIS.close()
        _REDIS = None
