from __future__ import annotations

from auth.config import Settings


class MongoAuditRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        raise NotImplementedError("TODO: sync Mongo log_event")

    def list_events(self, account_id: int, limit: int = 5):
        raise NotImplementedError("TODO: sync Mongo list_events")

    def clear(self) -> None:
        raise NotImplementedError("TODO: sync Mongo clear")


class AsyncMongoAuditRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        raise NotImplementedError("TODO: async Mongo log_event")

    async def list_events(self, account_id: int, limit: int = 5):
        raise NotImplementedError("TODO: async Mongo list_events")

    async def clear(self) -> None:
        raise NotImplementedError("TODO: async Mongo clear")
