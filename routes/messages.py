from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from blob_db import get_db, make_blob_id

router = APIRouter(prefix="/messages")


class MessageIn(BaseModel):
    data: str
    wrapped_key: str
    iv: str


class Message(MessageIn):
    message_id: str
    created_at: str


@router.post("", status_code=201)
def create_message(msg: MessageIn):
    try:
        db = get_db()
        message_id = make_blob_id()
        db.execute(
            "INSERT INTO encrypted_messages (message_id, data, wrapped_key, iv) VALUES (?, ?, ?, ?)",
            (message_id, msg.data, msg.wrapped_key, msg.iv),
        )
        db.commit()
        return {"message_id": message_id}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to store message")


@router.get("")
def list_messages():
    db = get_db()
    rows = db.execute(
        "SELECT message_id, data, wrapped_key, iv, created_at FROM encrypted_messages ORDER BY created_at DESC"
    ).fetchall()
    return [
        Message(
            message_id=r["message_id"],
            data=r["data"],
            wrapped_key=r["wrapped_key"],
            iv=r["iv"],
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.delete("/{message_id}", status_code=204)
def delete_message(message_id: str):
    db = get_db()
    cur = db.execute(
        "DELETE FROM encrypted_messages WHERE message_id = ?", (message_id,)
    )
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Message not found")
