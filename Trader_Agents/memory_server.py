from mcp.server.fastmcp import FastMCP
from typing import Optional, List, Dict, Any
import sqlite3
from contextlib import closing
import os


def _ensure_db(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with closing(sqlite3.connect(path)) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT, namespace TEXT, key TEXT, value TEXT)"
        )
        conn.commit()


class MemoryStore:
    def __init__(self, db_path: str):
        _ensure_db(db_path)
        self.db_path = db_path

    def put(self, namespace: str, key: str, value: str) -> int:
        with closing(sqlite3.connect(self.db_path)) as conn:
            cur = conn.execute(
                "INSERT INTO memory(namespace, key, value) VALUES(?,?,?)",
                (namespace, key, value),
            )
            conn.commit()
            return int(cur.lastrowid)

    def get(self, namespace: str, key: str) -> Optional[str]:
        with closing(sqlite3.connect(self.db_path)) as conn:
            cur = conn.execute(
                "SELECT value FROM memory WHERE namespace=? AND key=? ORDER BY id DESC LIMIT 1",
                (namespace, key),
            )
            row = cur.fetchone()
            return row[0] if row else None

    def list(self, namespace: str) -> List[Dict[str, Any]]:
        with closing(sqlite3.connect(self.db_path)) as conn:
            cur = conn.execute(
                "SELECT id, key, value FROM memory WHERE namespace=? ORDER BY id DESC",
                (namespace,),
            )
            return [
                {"id": row[0], "key": row[1], "value": row[2]}
                for row in cur.fetchall()
            ]


mcp = FastMCP("memory_server")


@mcp.tool()
async def memory_put(namespace: str, key: str, value: str, db_path: str = "./memory/local.db") -> int:
    """Store a value by namespace and key, returns entry id."""
    store = MemoryStore(db_path)
    return store.put(namespace, key, value)


@mcp.tool()
async def memory_get(namespace: str, key: str, db_path: str = "./memory/local.db") -> Optional[str]:
    """Get a value by namespace and key."""
    store = MemoryStore(db_path)
    return store.get(namespace, key)


@mcp.tool()
async def memory_list(namespace: str, db_path: str = "./memory/local.db") -> List[Dict[str, Any]]:
    """List values in a namespace (latest first)."""
    store = MemoryStore(db_path)
    return store.list(namespace)


if __name__ == "__main__":
    mcp.run(transport="stdio")


