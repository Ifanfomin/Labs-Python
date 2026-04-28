from __future__ import annotations

from typing import Protocol

from auth.models import Account, AuditEvent


class AccountsRepositoryProtocol(Protocol):
    def create_account(self, email: str) -> Account:
        ...

    def get_account(self, account_id: int) -> Account | None:
        ...

    def clear(self) -> None:
        ...


class AuditRepositoryProtocol(Protocol):
    def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        ...

    def list_events(self, account_id: int, limit: int = 5) -> list[AuditEvent]:
        ...

    def clear(self) -> None:
        ...


class CodeRepositoryProtocol(Protocol):
    def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        ...

    def has_code(self, account_id: int) -> bool:
        ...

    def clear(self) -> None:
        ...


class AsyncAccountsRepositoryProtocol(Protocol):
    async def create_account(self, email: str) -> Account:
        ...

    async def get_account(self, account_id: int) -> Account | None:
        ...

    async def clear(self) -> None:
        ...


class AsyncAuditRepositoryProtocol(Protocol):
    async def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        ...

    async def list_events(self, account_id: int, limit: int = 5) -> list[AuditEvent]:
        ...

    async def clear(self) -> None:
        ...


class AsyncCodeRepositoryProtocol(Protocol):
    async def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        ...

    async def has_code(self, account_id: int) -> bool:
        ...

    async def clear(self) -> None:
        ...
