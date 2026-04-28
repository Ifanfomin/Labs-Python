from __future__ import annotations

from auth.config import Settings


class PostgresAccountsRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def create_account(self, email: str):
        raise NotImplementedError("TODO: sync PostgreSQL create_account")

    def get_account(self, account_id: int):
        raise NotImplementedError("TODO: sync PostgreSQL get_account")

    def clear(self) -> None:
        raise NotImplementedError("TODO: sync PostgreSQL clear")


class AsyncPostgresAccountsRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def create_account(self, email: str):
        raise NotImplementedError("TODO: async PostgreSQL create_account")

    async def get_account(self, account_id: int):
        raise NotImplementedError("TODO: async PostgreSQL get_account")

    async def clear(self) -> None:
        raise NotImplementedError("TODO: async PostgreSQL clear")
