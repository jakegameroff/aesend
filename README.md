# AESend

End-to-end encrypted messaging. The server manages mailboxes and stores opaque ciphertext — it never sees plaintext or decryption keys.

## How it works

1. A user registers a username and uploads their RSA public key to create a mailbox
2. A sender's browser fetches the recipient's public key, generates a random AES-256 key, encrypts the message with AES-GCM, wraps the AES key with the recipient's RSA public key, and sends everything to the server
3. The recipient fetches their messages and decrypts in-browser with their private key, which never leaves their device

RSA-OAEP 4096-bit + AES-256-GCM hybrid encryption, Web Crypto API.

## API

### Mailboxes

| Method | Endpoint | Body | Response | Status |
|--------|----------|------|----------|--------|
| `POST` | `/mailboxes` | `{"username": "...", "public_key": "..."}` | `{"username": "..."}` | `201` |
| `GET` | `/mailboxes/{username}` | — | `{"public_key": "..."}` | `200` |

### Messages

| Method | Endpoint | Body | Response | Status |
|--------|----------|------|----------|--------|
| `POST` | `/messages` | `{"data": "...", "wrapped_key": "...", "iv": "...", "username": "..."}` | `{"message_id": "..."}` | `201` |
| `GET` | `/messages/{username}` | — | `[{"message_id", "username", "data", "wrapped_key", "iv", "created_at"}, ...]` | `200` |

Errors return `{"detail": "message"}` with `400`, `404`, `409`, or `500`.

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
