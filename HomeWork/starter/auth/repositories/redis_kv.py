from __future__ import annotations

from auth.config import Settings


class RedisCodeRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        raise NotImplementedError("TODO: sync Redis set_code")

    def has_code(self, account_id: int) -> bool:
        raise NotImplementedError("TODO: sync Redis has_code")

    def clear(self) -> None:
        raise NotImplementedError("TODO: sync Redis clear")


class AsyncRedisCodeRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        raise NotImplementedError("TODO: async Redis set_code")

    async def has_code(self, account_id: int) -> bool:
        raise NotImplementedError("TODO: async Redis has_code")

    async def clear(self) -> None:
        raise NotImplementedError("TODO: async Redis clear")
