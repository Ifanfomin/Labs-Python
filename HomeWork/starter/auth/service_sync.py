from __future__ import annotations

from auth.protocols import (
    AccountsRepositoryProtocol,
    AuditRepositoryProtocol,
    CodeRepositoryProtocol,
)


class AccountCardService:
    def __init__(
        self,
        accounts: AccountsRepositoryProtocol,
        audit: AuditRepositoryProtocol,
        codes: CodeRepositoryProtocol,
    ) -> None:
        self.accounts = accounts
        self.audit = audit
        self.codes = codes

    def create_account(self, email: str):
        raise NotImplementedError("TODO: создать аккаунт и записать событие в audit")

    def set_verification_code(self, account_id: int, ttl_seconds: int = 300):
        raise NotImplementedError("TODO: сгенерировать код, положить в Redis и записать событие")

    def get_account_card(self, account_id: int):
        raise NotImplementedError("TODO: собрать account + has_active_code + events")

    def reset(self) -> None:
        raise NotImplementedError("TODO: очистить все 3 хранилища")
