# RAG Bot Architecture Overview

## 1. High-Level System Architecture

The RAG Bot application implements a standard client-server architecture with Retrieval-Augmented Generation (RAG) capabilities to anchor AI responses to user-provided documents.

The system consists of the following major components:

- **Client (Frontend)**: React Single-Page Application (SPA) built with Vite.
- **Web Server (Backend)**: Python FastAPI application handling HTTP requests, authentication, and processing data.
- **Relational Database**: Local SQLite (via SQLAlchemy) storing user metadata, document tracking, and chat history.
- **Vector Database**: Pinecone for storing and retrieving high-dimensional document embeddings.
- **LLM Provider**: OpenAI (or Google Gemini/Groq depending on usage configuration) for generating final responses.

---

## 2. Core Functional Flows

### A. Document Ingestion Flow

When a user uploads a document, the following sequence occurs:

1.  **Upload**: The frontend sends the raw file (PDF, DOCX, TXT) via multipart/form-data to the `/documents/upload` API.
2.  **Validation**: The backend checks the file extension and verifies JWT authorization.
3.  **Extraction**: Raw text is extracted using appropriate libraries (`PyPDF2`, `python-docx`).
4.  **Chunking**: The text is split into smaller, manageable chunks (e.g., 1000 characters with 200 character overlap) to preserve context.
5.  **Embedding**: Each chunk is passed to an embedding model to generate a numerical vector representation.
6.  **Storage**:
    - The vectors and their associated metadata (text chunk, original filename, `user_id`) are pushed to **Pinecone**.
    - Metadata about the document upload (filename, timestamp) is saved to the **SQLite database**.
    - A local copy of the file is deposited in the `/uploads` directory.

### B. Query and Retrieval Flow (The RAG process)

1.  **Query Input**: User submits a question through the chat interface.
2.  **Query Embedding**: The backend converts the user's natural language query into a vector using the _exact same_ embedding model used during document ingestion.
3.  **Similarity Search (Retrieval)**: The backend queries Pinecone with the vector.
    - _Security Note_: A metadata filter on `user_id` is applied so users only retrieve chunks from their _own_ documents.
4.  **Context Assembly**: Pinecone returns the top-K most similar text chunks. By combining these chunks, the backend forms a "Context Window".
5.  **Generation**: The backend sends a prompt to the LLM (e.g., OpenAI) containing:
    - The user's original query.
    - The assembled Context Window.
    - System instructions to answer _only_ based on the context.
6.  **Response**: The LLM output is returned to the user, alongside the source materials (filenames) used to form the context.
