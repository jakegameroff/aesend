import secrets
import sqlite3

DB = "/data/blobs.db"


def make_blob_id() -> str:
    return secrets.token_urlsafe(32)


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS encrypted_blobs (
            blob_id TEXT PRIMARY KEY NOT NULL,
            data BLOB NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()
