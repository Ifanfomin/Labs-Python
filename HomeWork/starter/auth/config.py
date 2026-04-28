from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    postgres_dsn: str
    mongo_dsn: str
    mongo_db_name: str
    redis_dsn: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            postgres_dsn=os.getenv(
                "POSTGRES_DSN",
                "postgresql://postgres:postgres@localhost:5432/homework_auth",
            ),
            mongo_dsn=os.getenv("MONGO_DSN", "mongodb://localhost:27017"),
            mongo_db_name=os.getenv("MONGO_DB_NAME", "homework_auth"),
            redis_dsn=os.getenv("REDIS_DSN", "redis://localhost:6379/0"),
        )
