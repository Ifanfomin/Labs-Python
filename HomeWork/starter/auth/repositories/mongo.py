from __future__ import annotations

from auth.config import Settings
from auth.models import AuditEvent
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

class MongoAuditRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = MongoClient(settings.mongo_dsn)
        self.db = self.client[settings.mongo_db_name]
        self.collection = self.db["audit_events"]

    def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        event = {
            "account_id": account_id,
            "event_type": event_type,
            "payload": payload,
            "created_at": datetime.now().isoformat()
        }
        self.collection.insert_one(event)

    def list_events(self, account_id: int, limit: int = 5) -> list[AuditEvent]:
        events = self.collection.find(
            {"account_id": account_id},
            {"_id": 0}
        ).sort("created_at", -1).limit(limit)
        return [
            AuditEvent(
                account_id=event["account_id"],
                event_type=event["event_type"],
                payload=event["payload"],
                created_at=datetime.fromisoformat(event["created_at"])
            )
            for event in events
        ]

    def clear(self) -> None:
        self.collection.delete_many({})

    def __del__(self):
        self.client.close()

class AsyncMongoAuditRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        self.client = AsyncIOMotorClient(settings.mongo_dsn)
        self.db = self.client[settings.mongo_db_name]
        self.collection = self.db["audit_events"]

    async def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        event = {
            "account_id": account_id,
            "event_type": event_type,
            "payload": payload,
            "created_at": datetime.now().isoformat(),
        }

        await self.collection.insert_one(event)

    async def list_events(self, account_id: int, limit: int = 5) -> list[AuditEvent]:
        cursor = (
            self.collection.find(
                {"account_id": account_id},
                {"_id": 0},
            )
            .sort("created_at", -1)
            .limit(limit)
        )

        events = await cursor.to_list(length=limit)

        return [
            AuditEvent(
                account_id=event["account_id"],
                event_type=event["event_type"],
                payload=event["payload"],
                created_at=datetime.fromisoformat(
                    event["created_at"]
                ),
            )
            for event in events
        ]

    async def clear(self) -> None:
        await self.collection.delete_many({})

    def __del__(self):
        self.client.close()