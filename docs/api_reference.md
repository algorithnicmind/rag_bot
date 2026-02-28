# API Reference

The FastAPI backend runs on `http://127.0.0.1:8000/` and provides a set of RESTful endpoints.

## Base URL

`/` : Returns `{"Hello": "Welcome to RAG Bot API"}`

---

## Authentication Endpoints

### 1. Register User

`POST /auth/register`

- **Request Body**:
  - `username` (str): Unique identifier.
  - `email` (str): Unique email address.
  - `password` (str): Secret plaintext password (hashed on server).
- **Response**: `200 OK`
  - Returns the created user object (excluding the password).

### 2. Login User

`POST /auth/login`

- **Request Form-Data** (OAuth2):
  - `username` (str): Registered username.
  - `password` (str): Password.
- **Response**: `200 OK`
  - `access_token` (str): JWT Token valid for session (usually 30 minutes).
  - `token_type` (str): "bearer"

### 3. Get Current User (Me)

`GET /users/me`

- **Headers**: `Authorization: Bearer <token>`
- **Response**: `200 OK`
  - `id` (int): User ID.
  - `username` (str): User's username.

---

## Document Endpoints

### 4. Upload Document

`POST /documents/upload`

- **Headers**: `Authorization: Bearer <token>`
- **Request Body (Multipart Form)**:
  - `file` (File): Only `.pdf`, `.docx`, and `.txt` are accepted.
- **Response**: `200 OK`
  - `id` (int): Document ID.
  - `filename` (str): Original filename.
  - `upload_date` (str): Timestamp of ingestion.

### 5. Retrieve User Documents

`GET /documents`

- **Headers**: `Authorization: Bearer <token>`
- **Response**: `200 OK`
  - Returns a list of documents uploaded by the authenticated user.

---

## Chat Execution

### 6. Chat with RAG Engine

`POST /chat`

- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  - `query` (str): The specific question or prompt the user wishes to ask based on their documents.
- **Response**: `200 OK`
  - `answer` (str): The AI-generated answer.
  - `sources` (list of str): Filenames from which the context was drawn.
