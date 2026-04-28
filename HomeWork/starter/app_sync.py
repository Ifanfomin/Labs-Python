from auth import AccountCardService, Settings
from auth.repositories import MongoAuditRepository, PostgresAccountsRepository, RedisCodeRepository


def main() -> None:
    settings = Settings.from_env()
    service = AccountCardService(
        accounts=PostgresAccountsRepository(settings),
        audit=MongoAuditRepository(settings),
        codes=RedisCodeRepository(settings),
    )

    service.reset()
    try:
        account = service.create_account("student@example.com")
        service.set_verification_code(account.id, ttl_seconds=60)

        card = service.get_account_card(account.id)
        assert card.account.email == "student@example.com"
        assert card.has_active_code is True
        assert [event.event_type for event in card.events[:2]] == [
            "verification_code_set",
            "account_created",
        ]
        print("sync scenario is OK")
    finally:
        service.reset()


if __name__ == "__main__":
    main()
