from typing import Any, Dict
import aiosqlite

from src.libs.dbms_client.dbms_client_contract import DbmsClientContract
from src.libs.dbms_client.types.dbms_client_types import (
    DBClientInitArgs,
    DBExecuteArgs,
    DBInitializeArgs,
)


class SqliteClient(DbmsClientContract):
    def __init__(self, args: DBClientInitArgs) -> None:
        self._db_path = args.db_path
        self._conn: aiosqlite.Connection

    async def initialize(self, args: DBInitializeArgs) -> None:
        await self.connect()
        await self._conn.execute("PRAGMA journal_mode=WAL;")
        await self._conn.execute("BEGIN;")
        try:
            for sql in args.sql_schemas:
                await self._conn.execute(sql)
            await self._conn.commit()

        except Exception:
            await self._conn.rollback()
            raise
        finally:
            await self.close()

    async def connect(self) -> None:
        if self._conn:
            return
        self._conn = await aiosqlite.connect(self._db_path, timeout=5)
        await self._conn.execute("PRAGMA foreign_keys = ON;")

    async def execute(self, args: DBExecuteArgs) -> Dict[str, Any] | None:
        await self.connect()

        try:
            async with self._conn.execute(args.query) as cursor:
                if args.query.strip().upper().startswith("SELECT"):
                    return await cursor.fetchall()
                else:
                    await self._conn.commit()
                    return None
        except Exception as e:
            raise RuntimeError(f"Query failed: {e}")

    async def close(self) -> None:
        if self._conn:
            await self._conn.close()
            self._conn = None
