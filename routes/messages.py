from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db import get_db, make_id

router = APIRouter(prefix="/messages")

class MessageIn(BaseModel):
    data: str
    wrapped_key: str
    iv: str
    username: str

class Message(MessageIn):
    message_id: str
    created_at: str

@router.post("", status_code=201)
def create_message(msg: MessageIn):
    try:
        db = get_db()
        message_id = make_id()
        db.execute(
            "INSERT INTO encrypted_messages (message_id, mailbox_id, data, wrapped_key, iv) VALUES (?, ?, ?, ?, ?)",
            (message_id, msg.username, msg.data, msg.wrapped_key, msg.iv),
        )
        db.commit()
        return {"message_id": message_id}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to store message")

@router.get("/{username}")
def list_messages(username: str):
    db = get_db()
    rows = db.execute(
        "SELECT message_id, mailbox_id, data, wrapped_key, iv, created_at FROM encrypted_messages WHERE mailbox_id = ? ORDER BY created_at DESC",
        (username,),
    ).fetchall()
    return [
        Message(
            message_id=r["message_id"],
            username=r["mailbox_id"],
            data=r["data"],
            wrapped_key=r["wrapped_key"],
            iv=r["iv"],
            created_at=r["created_at"],
        )
        for r in rows
    ]
