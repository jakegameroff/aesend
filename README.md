# AESend

Zero-knowledge encrypted sharing. Send anything to anyone — the server never sees what you send.

AESend encrypts your data in the browser using AES before it ever leaves your device. The backend stores nothing but opaque ciphertext. No accounts, no tracking, no metadata. Just a link and a secret only you and your recipient know.

## How it works

1. You drop in a file or message on the frontend
2. AESend encrypts it client-side with AES — the plaintext never leaves your browser
3. The ciphertext is sent to the backend, which stores the blob and hands back a unique URL-safe ID
4. Share the link. The recipient opens it, decrypts in their browser. Done.

The server is intentionally blind. It stores encrypted bytes and nothing else. Even if the database leaked, the contents are meaningless without the key — which never touches the network.

## API

All endpoints are under `/blobs`. Data is sent/received as base64-encoded bytes.

| Method | Endpoint | Body | Response | Status |
|--------|----------|------|----------|--------|
| `POST` | `/blobs` | `{"data": "<base64>"}` | `{"blob_id": "...", "data": "<base64>"}` | `201` |
| `GET` | `/blobs/{blob_id}` | — | `{"data": "<base64>"}` | `200` |
| `GET` | `/blobs` | — | `{"blobs": ["id1", "id2", ...]}` | `200` |
| `DELETE` | `/blobs/{blob_id}` | — | — | `204` |

### Errors

All errors return `{"detail": "message"}`:

- `404` — Blob not found (GET or DELETE with bad id)
- `422` — Invalid request body (bad JSON, missing fields)
- `500` — Failed to create blob (DB error)

## Run

```
pip install -r requirements.txt
uvicorn main:app --reload
```

Or with Docker:

```
docker build -t aesend .
docker run -p 8000:8000 aesend
```

## Stack

- Python + FastAPI
- SQLite
- No ORM, no auth, no encryption server-side — by design
