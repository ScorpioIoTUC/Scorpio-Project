from src.libs.dbms_client import (
    DbmsClient,
    DBClientInitArgs,
    DBExecuteArgs,
    DBInitializeArgs,
)
from src.libs.zero_dependency.datetime_utils import datetime_to_string, now

CLIENT_NAME = "sqlite"
SCHEMAS = [
    """
    CREATE TABLE IF NOT EXISTS local_backup (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payload TEXT NOT NULL,
        topic TEXT NOT NULL,
        uploaded BOOLEAN NOT NULL DEFAULT 0,
        creation_datetime TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
        update_datetime TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
    )
    """
]


class Database:
    def __init__(self, db_path: str) -> None:
        self.client = DbmsClient(
            DBClientInitArgs(client_name=CLIENT_NAME, db_path=db_path)
        )

    def _current_datetime(self) -> str:
        return datetime_to_string(now(), format_string="%Y-%m-%d %H:%M:%S")

    async def create(self):
        await self.client.initialize(DBInitializeArgs(sql_schemas=SCHEMAS))

    async def insert(self, topic: str, payload: str):
        current_datetime = self._current_datetime()
        query = f"""
        INSERT INTO local_backup (payload, topic, uploaded, creation_datetime, update_datetime) 
        VALUES ({payload}, {topic}, 0, {current_datetime}, {current_datetime})
        """
        await self.client.execute(DBExecuteArgs(query))

    async def insert_many(self, entries: list[tuple[str, str]]):
        current_datetime = self._current_datetime()
        values_str = ", ".join(
            f"({payload}, {topic}, 0, {current_datetime}, {current_datetime})"
            for topic, payload in entries
        )
        query = f"""
        INSERT INTO local_backup (payload, topic, uploaded, creation_datetime, update_datetime) 
        VALUES {values_str}
        """
        await self.client.execute(DBExecuteArgs(query))

    async def find_all(self, uploaded: bool = False):
        uploaded_val = 1 if uploaded else 0
        query = f"""
        SELECT id, payload, topic, creation_datetime, update_datetime 
        FROM local_backup 
        WHERE uploaded = {uploaded_val}
        """
        return await self.client.execute(DBExecuteArgs(query))

    async def update_many(self, ids: list[int], uploaded: bool = True):
        current_datetime = self._current_datetime()
        ids_str = ", ".join(str(id) for id in ids)
        uploaded_val = 1 if uploaded else 0
        query = f"""
        UPDATE local_backup 
        SET uploaded = {uploaded_val}, update_datetime = {current_datetime} 
        WHERE id IN ({ids_str})
        """
        await self.client.execute(DBExecuteArgs(query))

    async def delete_many(self, ids: list[int]):
        query = f"""
        DELETE FROM local_backup 
        WHERE id IN ({", ".join(str(id) for id in ids)})
        """
        await self.client.execute(DBExecuteArgs(query))
        
    async def end_connection(self):
        await self.client.close()
