from __future__ import annotations

from auth.config import Settings
from auth.models import Account
from auth.exceptions import AccountNotFoundError

import psycopg

class PostgresAccountsRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.conn = psycopg.connect(settings.postgres_dsn)
        self._create_tables()
    
    def _create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(100) UNIQUE NOT NULL
                )
            """)
            self.conn.commit()

    def create_account(self, email: str):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO accounts (email) VALUES (%s) RETURNING id, email",
                (email,)
            )
            result = cur.fetchone()
            account = Account(result[0], result[1])

            self.conn.commit()
            return account

    def get_account(self, account_id: int):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, email FROM accounts WHERE id = %s",
                (account_id, )
            )

            result = cur.fetchone()
            if result:
                account = Account(result[0], result[1])
            else:
                raise AccountNotFoundError(f"Account with id {account_id} not found")

            return account
    
    def clear(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """)
            tables = cur.fetchall()

            for table in tables:
                table_name = table[0]
                cur.execute(f"TRUNCATE TABLE {table_name} CASCADE")
            
            self.conn.commit()
    
    def __del__(self):
        self.conn.close()


class AsyncPostgresAccountsRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._create_tables()
    
    def _create_tables(self):
        with psycopg.connect(self.settings.postgres_dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS accounts (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(100) UNIQUE NOT NULL
                    )
                """)
                conn.commit()

    async def create_account(self, email: str):
        async with await psycopg.AsyncConnection.connect(self.settings.postgres_dsn) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO accounts (email) VALUES (%s) RETURNING id, email",
                    (email,)
                )
                result = await cur.fetchone()
                account = Account(result[0], result[1])

                await conn.commit()
                return account

    async def get_account(self, account_id: int):
        async with await psycopg.AsyncConnection.connect(self.settings.postgres_dsn) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT id, email FROM accounts WHERE id = %s",
                    (account_id, )
                )

                result = await cur.fetchone()
                if result:
                    account = Account(result[0], result[1])
                else:
                    raise AccountNotFoundError(f"Account with id {account_id} not found")

                return account

    async def clear(self) -> None:
        async with await psycopg.AsyncConnection.connect(self.settings.postgres_dsn) as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)
                tables = await cur.fetchall()

                for table in tables:
                    table_name = table[0]
                    await cur.execute(f"TRUNCATE TABLE {table_name} CASCADE")

                await conn.commit()
