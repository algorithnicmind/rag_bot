# RAG Bot — Project Plan

## Overview

A full-stack **Retrieval-Augmented Generation (RAG)** web application that allows users to securely upload documents (PDF, DOCX, TXT) and have intelligent, AI-powered conversations about their content. The AI only answers from your documents — no hallucinations.

## Tech Stack

| Layer                   | Technology                                             |
| ----------------------- | ------------------------------------------------------ |
| **Frontend**            | React 19 + Vite                                        |
| **Backend API**         | Python + FastAPI                                       |
| **Auth**                | JWT (JSON Web Tokens) via `python-jose` + `passlib`    |
| **Database**            | SQLite (via SQLAlchemy ORM)                            |
| **Vector Database**     | Pinecone (Serverless, AWS us-east-1)                   |
| **Embeddings**          | Google Gemini `gemini-embedding-001` (3072 dimensions) |
| **LLM**                 | Google Gemini `gemini-2.0-flash`                       |
| **Document Processing** | PyPDF, python-docx                                     |
| **RAG Framework**       | LangChain                                              |

## Implementation Steps

1. **Step 1: Project Setup** — Initialize React frontend (Vite) and FastAPI backend with virtual environment.
2. **Step 2: Authentication** — User Registration and Login APIs with JWT. Password hashing with bcrypt.
3. **Step 3: Document Upload** — Build upload UI and Python endpoints to extract text from PDF/Word/Text files.
4. **Step 4: Vectorization (RAG Core)** — Chunk text using `RecursiveCharacterTextSplitter`, convert to embeddings via Gemini, store in Pinecone with user-scoped metadata.
5. **Step 5: Chat Interface** — Build chat UI with markdown rendering, implement retrieval with user-scoped filtering, and generate LLM responses via Gemini.
6. **Step 6: Error Handling** — Graceful user-facing error messages for rate limits, network issues, and model errors.
7. **Step 7: Documentation** — Comprehensive docs, README, and `.gitignore` for a clean, production-ready repository.

## Project Status: ✅ Complete

All 7 steps have been implemented and verified.
