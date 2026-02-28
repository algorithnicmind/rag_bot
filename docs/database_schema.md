# Database Schema

The RAG Bot relies on two distinct databases for operation.

1.  **Local Relational Database**: SQLite via SQLAlchemy. It manages primary entities like Users and document metadata.
2.  **Vector Database**: Pinecone (via `pinecone-client`). It holds high-dimensional embeddings for similarity search.

---

## 1. Local SQLite Models

The local application state is defined inside `backend/models.py`.

### User Model Actions

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
```

- `id`: Auto-incrementing primary key. It serves as the unique identifier for `user_id` inside Pinecone metadata filters.
- `username` & `email`: Uniquely identifying attributes ensuring no collision during `/auth/register`.
- `hashed_password`: Handled by `passlib` context (`bcrypt`), securely validating against user payloads during `/auth/login`.

### Document Model Actions

```python
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    filename = Column(String, index=True)
    upload_date = Column(String)
```

- `user_id`: Foreign key equivalent pointing back to the `User.id` attempting to log a document upload.
- `filename`: A reference corresponding exactly to the name preserved in the physical `/uploads` folder.

---

## 2. Vector Database Storage Schema (Pinecone)

The `pinecone` client creates vector entries shaped around extracted chunks of a document. It utilizes an embedding dimension dictated by the underlying LLM choice.

```text
Pinecone Record Component:
{
    id: "chunk-uuid",         # A globally unique string ID
    values: [0.32, -0.1, ...], # The 768 or 1536 float array (vector representation)
    metadata: {
        text: "The literal text extracted from the document that was embedded.",
        user_id: 1,           # Linking the chunk back to the SQLite User.id
        filename: "HR-Policies.pdf"
    }
}
```

This strict metadata schema provides the magic behind secure retrieval. Since `user_id` is assigned at the chunk level during `process_and_store_text()`, similarity searches can be passed a filter parameter dictating that Pinecone _only_ searches records whose `user_id` matches the active JWT session user.
