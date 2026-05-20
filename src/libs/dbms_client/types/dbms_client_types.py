from dataclasses import dataclass
from typing import List


@dataclass
class DBClientInitArgs:
    client_name: str
    db_path: str


@dataclass 
class DBInitializeArgs:
    sql_schemas: List[str]

@dataclass
class DBExecuteArgs:
    query: str
