# RAG Bot Project Plan

## Overview

A Prototype Retrieval-Augmented Generation (RAG) web application allowing users to securely chat with their uploaded documents.

## Tech Stack

- **Backend:** Python with FastAPI
- **Frontend:** React (Vite)
- **Database (User/Metadata):** SQLite (Local prototype), scalable to PostgreSQL (Render/Neon)
- **Vector Database:** Pinecone or Qdrant (Free tier cloud)
- **Language Model:** Google Gemini API / Groq API (Free tier)
- **Authentication:** JWT
- **Document Processing:** Langchain (PyPDF2 for PDF, python-docx for Word)

## Implementation Steps

1. **Step 1: Project Setup** - Initialize React frontend and FastAPI backend.
2. **Step 2: Authentication** - User Registration and Login APIs with JWT.
3. **Step 3: Document Upload** - Build upload UI and Python endpoints to extract text from PDF/Word/Text files.
4. **Step 4: Vectorization (RAG Core)** - Chunk text, convert to embeddings, save in Vector DB.
5. **Step 5: Chat Interface** - Build chat UI, implement retrieval, and stream LLM responses.
