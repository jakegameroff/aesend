from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db import get_db
import re

router = APIRouter(prefix="/mailboxes")

USERNAME_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{1,30}[a-z0-9]$")

class MailboxIn(BaseModel):
    username: str
    public_key: str

@router.get("")
def list_mailboxes():
    db = get_db()
    rows = db.execute(
        "SELECT mailbox_id, created_at FROM mailboxes ORDER BY created_at DESC"
    ).fetchall()
    return [{"username": r["mailbox_id"], "created_at": r["created_at"]} for r in rows]

@router.post("", status_code=201)
def create_mailbox(body: MailboxIn):
    username = body.username.lower().strip()
    if not USERNAME_RE.match(username):
        raise HTTPException(
            status_code=400,
            detail="Username must be 3-32 characters, lowercase letters, numbers, hyphens, and underscores.",
        )
    db = get_db()
    existing = db.execute(
        "SELECT 1 FROM mailboxes WHERE mailbox_id = ?", (username,)
    ).fetchone()
    if existing:
        raise HTTPException(status_code=409, detail="Username already taken")
    try:
        db.execute(
            "INSERT INTO mailboxes (mailbox_id, public_key) VALUES (?, ?)",
            (username, body.public_key),
        )
        db.commit()
        return {"username": username}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create mailbox")

@router.get("/{username}")
def get_mailbox(username: str):
    db = get_db()
    row = db.execute(
        "SELECT public_key FROM mailboxes WHERE mailbox_id = ?", (username,)
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Mailbox not found")
    return {"public_key": row["public_key"]}
