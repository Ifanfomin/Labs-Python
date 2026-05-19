from __future__ import annotations

from auth.config import Settings
import redis
from redis.asyncio import Redis

class RedisCodeRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = redis.Redis.from_url(settings.redis_dsn)

    def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        key = str(account_id)
        self.client.setex(key, ttl_seconds, code)

    def has_code(self, account_id: int) -> bool:
        key = str(account_id)
        return self.client.exists(key) == 1

    def clear(self) -> None:
        self.client.flushdb()

    def __del__(self):
        self.client.close()


class AsyncRedisCodeRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = Redis.from_url(settings.redis_dsn)

    async def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        key = str(account_id)

        await self.client.setex(
            key,
            ttl_seconds,
            code,
        )

    async def has_code(self, account_id: int) -> bool:
        key = str(account_id)

        return await self.client.exists(key) == 1

    async def clear(self) -> None:
        await self.client.flushdb()

    async def close(self) -> None:
        await self.client.aclose()