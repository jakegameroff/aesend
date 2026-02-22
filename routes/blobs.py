from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from blob_db import get_db, make_blob_id

router = APIRouter(prefix="/blobs")

class BlobInit(BaseModel):
    data: bytes

class Blob(BlobInit):
    blob_id: str

@router.post("", status_code=201)
def create_blob(blob: BlobInit):
    try:
        db = get_db()
        blob_id = make_blob_id()
        db.execute("INSERT INTO encrypted_blobs (blob_id, data) VALUES (?, ?)",
            (blob_id, blob.data))
        db.commit()
        return Blob(blob_id=blob_id, data=blob.data)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create blob")

@router.get("/{blob_id}")
def get_blob(blob_id: str):
    db = get_db()
    result = db.execute("SELECT data FROM encrypted_blobs WHERE blob_id = ?", (blob_id,))
    row = result.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Blob not found")
    return {"data": row[0]}

@router.delete("/{blob_id}", status_code=204)
def delete_blob(blob_id: str):
    db = get_db()
    cur = db.execute("DELETE FROM encrypted_blobs WHERE blob_id = ?", (blob_id,))
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Blob not found")
