from .dbms_client_contract import DbmsClientContract
from .types.dbms_client_types import DBClientInitArgs, DBExecuteArgs, DBInitializeArgs


class DbmsClient(DbmsClientContract):
    CLIENTS = {"sqlite"}

    def __init__(self, args: DBClientInitArgs) -> None:
        if args.client_name not in DbmsClient.CLIENTS:
            msg = f"Unsupported client {args.client_name}"
            raise KeyError(msg)
        if args.client_name == "sqlite":
            from .clients.sqlite_client import SqliteClient # Lazy import

            self.client_obj = SqliteClient(args)
        self.client_name = args.client_name

    async def connect(self) -> None:
        return await self.client_obj.connect()

    async def initialize(self, args: DBInitializeArgs) -> None:
        return await self.client_obj.initialize(args)

    async def execute(self, args: DBExecuteArgs) -> dict | None:
        return await self.client_obj.execute(args)

    async def close(self) -> None:
        return await self.client_obj.close()
