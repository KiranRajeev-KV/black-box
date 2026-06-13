from contextlib import contextmanager
import sqlite3
from pathlib import Path
from typing import Iterator

DATABASE_PATH = Path("app.db")

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                password TEXT NOT NULL
            )
            """)
        
@contextmanager
def db_connection() -> Iterator[sqlite3.Connection]:
    connection = get_conn()

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()