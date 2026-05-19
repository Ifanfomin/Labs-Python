from __future__ import annotations

from random import randint

from auth.models import AccountCard
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
        # создать аккаунт в postgres
        account = await self.accounts.create_account(email)

        # записать событие в mongodb
        await self.audit.log_event(
            account.id,
            "account_created",
            {"email": email},
        )

        # вернуть account
        return account

    async def set_verification_code(
        self,
        account_id: int,
        ttl_seconds: int = 300,
    ):
        # сгенерировать код
        code = str(randint(1000, 9999))

        # положить код в redis
        await self.codes.set_code(
            account_id,
            code,
            ttl_seconds,
        )

        # записать событие в mongodb
        await self.audit.log_event(
            account_id,
            "verification_code_set",
            {"code": code},
        )

    async def get_account_card(self, account_id: int):
        # получить account из postgres
        account = await self.accounts.get_account(account_id)

        if account:
            account_id = account.id

            # проверить наличие кода в redis
            has_code = await self.codes.has_code(account_id)

            # получить события из mongodb
            events = await self.audit.list_events(account_id)

            card = AccountCard(
                account,
                has_code,
                events,
            )
        else:
            card = None

        return card

    async def reset(self) -> None:
        await self.accounts.clear()
        await self.audit.clear()
        await self.codes.clear()