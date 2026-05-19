from __future__ import annotations

from auth.models import AccountCard
from auth.protocols import (
    AccountsRepositoryProtocol,
    AuditRepositoryProtocol,
    CodeRepositoryProtocol,
)

from random import randint


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
            # Создть аккаунт, т.е. создать account.id и записать email и account.id в postgres
            account = self.accounts.create_account(email)

            # Запись событие создания аккаунта в mongodb
            self.audit.log_event(
                account.id,
                "account_created",
                {"email": email}
            )

            # вернуть account в котором есть и id и email
            return account

    def set_verification_code(self, account_id: int, ttl_seconds: int = 300):
        # сгеннерировать код, положить его в redis с ttl_seconds
        code = str(randint(1000, 9999))
        self.codes.set_code(account_id, code, ttl_seconds)
        
        # записать в mongodb событие о генереции кода
        self.audit.log_event(account_id, "verification_code_set", {"code": code})

    def get_account_card(self, account_id: int):
        # получить email из postgres
        account = self.accounts.get_account(account_id)
        if account:
            id = account.id
            has_code = self.codes.has_code(id)
            events = self.audit.list_events(id)

            card = AccountCard(account, has_code, events)
        else:
            card = None

        return card
    
    def reset(self) -> None:
        self.accounts.clear()
        self.audit.clear()
        self.codes.clear()
        