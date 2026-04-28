import asyncio

from auth import AsyncAccountCardService, Settings
from auth.repositories import (
    AsyncMongoAuditRepository,
    AsyncPostgresAccountsRepository,
    AsyncRedisCodeRepository,
)


async def main() -> None:
    settings = Settings.from_env()
    service = AsyncAccountCardService(
        accounts=AsyncPostgresAccountsRepository(settings),
        audit=AsyncMongoAuditRepository(settings),
        codes=AsyncRedisCodeRepository(settings),
    )

    await service.reset()
    try:
        first = await service.create_account("first@example.com")
        second = await service.create_account("second@example.com")

        await service.set_verification_code(first.id, ttl_seconds=60)
        await service.set_verification_code(second.id, ttl_seconds=60)

        first_card = await service.get_account_card(first.id)
        second_card = await service.get_account_card(second.id)
        
        assert first_card.has_active_code is True
        assert second_card.has_active_code is True
        print("async scenario is OK")
    finally:
        await service.reset()


if __name__ == "__main__":
    asyncio.run(main())
