# Application Security

The RAG Bot application implements several industry standard security mechanisms to guarantee that user data and company intellectual property (Documents) remain isolated between sessions.

## 1. Authentication (JWT Tokens)

- **Protocol**: OAuth2 standard using `PasswordRequestForm`.
- **Algorithm**: JSON Web Tokens (JWT) using `HS256` symmetric signing.
- **Dependency**: Relying exclusively on `python-jose` for deterministic token verification and decoding within FastAPI.

### Implementation:

Users send their username and password via `POST /auth/login`. If `passlib.bcrypt.verify` matches the hashed password saved inside SQLite, the backend responds with an encoded `access_token` bearing the `sub=user.username` payload.

Every subsequent request (uploading a file, listing files, executing a chat prompt) mandates the inclusion of standard authorization headers (`Authorization: Bearer <token>`).

## 2. Authorization (Role Based Access Control)

- **Dependency**: `FastAPI Depends(get_current_user)`

The backend does not support globally accessible chat interactions. The frontend is structurally incapable of routing users to the `Dashboard` unless a token resides in `localStorage`.

Once inside, `get_current_user` decodes the token, queries the active `User` model, and binds the request flow.

## 3. Data Isolation using Metadata Filtering

When documents are processed via LangChain and upserted to Pinecone:

```python
vector_store.process_and_store_text(
    text=extracted_text,
    user_id=current_user.id,
    filename=file.filename
)
```

Pinecone's storage mechanism forcibly injects `{"user_id": current_user.id}` into the vector record metadata.

When the user later types "Summarize my files" in chat:

```python
query_response = index.query(
    vector=embedding,
    top_k=5,
    include_metadata=True,
    filter={"user_id": user_id} # Extremely critical isolation tier
)
```

Because Pinecone strictly limits the search space via the `filter` argument, it becomes cryptographically and mathematically impossible for User A to retrieve or chat about User B's documents, regardless of whether similarities overlap.
