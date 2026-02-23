import secrets
import sqlite3

DB = "/data/aesend.db"


def make_id() -> str:
    return secrets.token_urlsafe(32)


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mailboxes (
            mailbox_id TEXT PRIMARY KEY NOT NULL,
            public_key TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS encrypted_messages (
            message_id TEXT PRIMARY KEY NOT NULL,
            mailbox_id TEXT,
            data TEXT NOT NULL,
            wrapped_key TEXT NOT NULL,
            iv TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    # Migration: add mailbox_id column to existing encrypted_messages tables
    try:
        conn.execute("ALTER TABLE encrypted_messages ADD COLUMN mailbox_id TEXT")
    except Exception:
        pass  # Column already exists
    conn.commit()
    conn.close()
