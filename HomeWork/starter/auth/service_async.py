from __future__ import annotations

from auth.protocols import (
    AsyncAccountsRepositoryProtocol,
    AsyncAuditRepositoryProtocol,
    AsyncCodeRepositoryProtocol,
)


class AsyncAccountCardService:
    def __init__(
        self,
        accounts: AsyncAccountsRepositoryProtocol,
        audit: AsyncAuditRepositoryProtocol,
        codes: AsyncCodeRepositoryProtocol,
    ) -> None:
        self.accounts = accounts
        self.audit = audit
        self.codes = codes

    async def create_account(self, email: str):
        raise NotImplementedError("TODO: async create_account")

    async def set_verification_code(self, account_id: int, ttl_seconds: int = 300):
        raise NotImplementedError("TODO: async set_verification_code")

    async def get_account_card(self, account_id: int):
        raise NotImplementedError("TODO: async get_account_card через asyncio.gather")

    async def reset(self) -> None:
        raise NotImplementedError("TODO: async очистка всех 3 хранилищ")
