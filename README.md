# AESend

Zero-knowledge encrypted sharing. The server never sees what you send.

Data is encrypted client-side with AES-256-GCM before it leaves the browser. The backend stores opaque ciphertext and nothing else. The key lives in the URL fragment, which browsers [never send to the server](https://www.rfc-editor.org/rfc/rfc3986#section-3.5).

## How it works

1. Enter a message on the frontend
2. Browser encrypts it with AES-256-GCM — plaintext never leaves your device
3. Ciphertext is sent to the backend, which stores the blob and returns a unique ID
4. Share the link. Recipient opens it, decrypts in their browser

The server is intentionally blind. Even if the database leaked, the contents are meaningless without the key.

## API

All endpoints under `/blobs`. Data is base64-encoded bytes.

| Method | Endpoint | Body | Response | Status |
|--------|----------|------|----------|--------|
| `POST` | `/blobs` | `{"data": "<base64>"}` | `{"blob_id": "...", "data": "<base64>"}` | `201` |
| `GET` | `/blobs/{blob_id}` | — | `{"data": "<base64>"}` | `200` |
| `DELETE` | `/blobs/{blob_id}` | — | — | `204` |

Errors return `{"detail": "message"}` with `404`, `422`, or `500`.

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

Python, FastAPI, SQLite.
