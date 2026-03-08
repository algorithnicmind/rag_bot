<div align="center">

# 🤖 RAG Bot

### _Your Personal AI Document Assistant_

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.134-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Vite](https://img.shields.io/badge/Vite-6.2-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-000000?style=for-the-badge)](https://pinecone.io)
[![Groq](https://img.shields.io/badge/Groq-AI-f55036?style=for-the-badge)](https://groq.com)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Embeddings-F5C018?style=for-the-badge)](https://huggingface.co)

**Upload your documents • Ask questions • Get AI-powered answers with source citations**

[Getting Started](#-getting-started) · [Features](#-features) · [Architecture](#-architecture) · [API Reference](#-api-endpoints) · [Documentation](#-documentation)

---

</div>

## 📖 About

**RAG Bot** is a full-stack web application that implements **Retrieval-Augmented Generation (RAG)** to let users securely upload documents and have intelligent conversations about their content. The AI answers _**only**_ from your documents — no hallucinations, no made-up facts.

Upload a PDF, Word document, or text file, and then ask questions like:

- _"Summarize the key points of this report"_
- _"What does section 3 say about the budget?"_
- _"Compare the findings from these two documents"_

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔐 Secure Authentication

- JWT-based registration & login
- bcrypt password hashing
- Token-protected API endpoints

### 📄 Smart Document Processing

- **PDF** support (via PyPDF)
- **Word .docx** support (via python-docx)
- **Plain text .txt** support
- Automatic text extraction & chunking

</td>
<td width="50%">

### 🧠 RAG-Powered AI Chat

- Powered by Groq LLaMA-3 (Fast Inference)
- Context-aware answers from YOUR docs only
- Source citations with every response
- Markdown-rendered AI responses

### 🔒 Data Isolation

- User-scoped vector storage
- Each user can only query their own documents
- Metadata filtering ensures zero data leakage

</td>
</tr>
</table>

---

## 🏗 Architecture

```
┌─────────────────┐       ┌─────────────────────────┐
│  React Frontend │ HTTP  │    FastAPI Backend       │
│  (Vite :5173)   │◄─────►│    (Uvicorn :8000)      │
│                 │ REST  │                         │
│  Login/Register │       │  Auth · Upload · Chat   │
│  Upload Docs    │       │  Document Processing    │
│  AI Chat UI     │       │  RAG Engine (LangChain) │
└─────────────────┘       └────┬──────────┬─────────┘
                               │          │
                          ┌────▼───┐  ┌───▼───────────┐
                          │ SQLite │  │ Pinecone Cloud │
                          │ Users  │  │ Vectors (384d) │
                          │ Docs   │  │ User-scoped    │
                          └────────┘  └───┬───────────┘
                                          │
                                    ┌─────▼───────────┐
                                    │ Groq & HF APIs  │
                                    │ Embedding + LLM │
                                    └─────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

| Tool    | Version Required |
| ------- | ---------------- |
| Python  | 3.10+            |
| Node.js | 20.19+ or 22.12+ |

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/rag_bot.git
cd rag_bot
```

### 2️⃣ Backend Setup

<details>
<summary><strong>🐍 Click to expand Backend instructions</strong></summary>
<br>

```bash
cd backend
python -m venv venv
```

**Activate virtual environment:**

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

> [!IMPORTANT]
> Create a `.env` file in the `backend/` directory with your API keys:

```env
GROQ_API_KEY="your-groq-api-key"
PINECONE_API_KEY="your-pinecone-api-key"
SECRET_KEY="any-random-secret-string"
```

| Key                | Where to get it                               |
| ------------------ | --------------------------------------------- |
| `GROQ_API_KEY`     | [Groq Console](https://console.groq.com/keys) |
| `PINECONE_API_KEY` | [Pinecone Console](https://app.pinecone.io)   |

**Start the server:**

```bash
python -m uvicorn main:app --reload
```

> [!TIP]
> Visit `http://127.0.0.1:8000/docs` for interactive Swagger API documentation.

</details>

### 3️⃣ Frontend Setup

<details>
<summary><strong>⚛️ Click to expand Frontend instructions</strong></summary>
<br>

Open a **new terminal** (keep the backend running):

```bash
cd frontend
npm install
```

> [!IMPORTANT]
> Create a `.env` file in the `frontend/` directory to connect to your backend:

```env
VITE_API_URL=http://127.0.0.1:8000
```

**Start the React app:**

```bash
npm run dev
```

> [!TIP]
> The app will be available at `http://localhost:5173`

</details>

---

## 📡 API Endpoints

| Method | Endpoint            | Auth | Description                                       |
| :----: | ------------------- | :--: | ------------------------------------------------- |
| `POST` | `/auth/register`    |  ❌  | Register a new user account                       |
| `POST` | `/auth/login`       |  ❌  | Login and receive JWT token                       |
| `GET`  | `/users/me`         |  🔐  | Get current user profile                          |
| `POST` | `/documents/upload` |  🔐  | Upload & vectorize a document (.pdf, .docx, .txt) |
| `GET`  | `/documents`        |  🔐  | List all uploaded documents                       |
| `POST` | `/chat`             |  🔐  | Ask a question about your documents               |

---

## 📁 Project Structure

```
rag_bot/
├── backend/
│   ├── main.py                # FastAPI app & routes
│   ├── auth.py                # JWT authentication logic
│   ├── models.py              # SQLAlchemy database models
│   ├── schemas.py             # Pydantic request/response schemas
│   ├── database.py            # SQLite connection setup
│   ├── document_processor.py  # PDF/DOCX/TXT text extraction
│   ├── vector_store.py        # Pinecone + HuggingFace embeddings
│   ├── rag_engine.py          # LangChain RAG pipeline
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # API keys (not committed)
│   ├── pytest.ini             # Pytest configuration
│   └── test/
│       ├── conftest.py        # Pytest fixtures & mock DB
│       ├── test_auth.py       # Auth unit tests
│       ├── test_documents.py  # File upload / isolation tests
│       └── test_chat.py       # RAG endpoint tests
│
├── frontend/
│   ├── src/
│   │   ├── api.js             # Centralized Axios & JWT interceptor
│   │   ├── App.jsx            # Root component & routing
│   │   ├── index.css          # Global dark theme styles
│   │   └── components/
│   │       ├── Login.jsx      # Auth forms
│   │       ├── Upload.jsx     # Document upload UI
│   │       └── Chat.jsx       # AI chat interface
│   ├── .env                   # API URL config (not committed)
│   └── package.json
│
├── docs/                      # Detailed documentation
│   ├── project_plan.md
│   ├── architecture.md
│   ├── api_reference.md
│   ├── frontend_guide.md
│   ├── database_schema.md
│   ├── security.md
│   └── setup_guide.md
│
├── .gitignore
└── README.md
```

---

## 📚 Documentation

Detailed documentation is available in the [`docs/`](./docs) folder:

| Document                                     | Description                                           |
| -------------------------------------------- | ----------------------------------------------------- |
| [Project Plan](./docs/project_plan.md)       | Overview, tech stack, and implementation timeline     |
| [Architecture](./docs/architecture.md)       | System design, data flows, and design decisions       |
| [API Reference](./docs/api_reference.md)     | Complete REST API documentation with examples         |
| [Frontend Guide](./docs/frontend_guide.md)   | React components, routing, and design system          |
| [Database Schema](./docs/database_schema.md) | SQLite models and Pinecone vector structure           |
| [Security](./docs/security.md)               | Authentication, data isolation, and secret management |
| [Setup Guide](./docs/setup_guide.md)         | Installation, configuration, and troubleshooting      |

---

## 🧪 Testing

The backend includes a comprehensive 29-test suite powered by **pytest**. Tests run on an isolated in-memory SQLite database and use mocked Google/Pinecone API calls so they are entirely free to run.

To execute the test suite:

```bash
cd backend
python -m pytest test/ -v
```

---

## 🔒 Security

> [!CAUTION]
> Never commit your `.env` file to GitHub. It is already excluded via `.gitignore`.

- **Passwords** are hashed with bcrypt — never stored in plaintext
- **JWT tokens** expire after 30 minutes
- **Document vectors** are user-scoped — users can only query their own data
- **API keys** are stored server-side only, never exposed to the frontend

---

## 🛠 Tech Stack

| Category          | Technology                                        |
| ----------------- | ------------------------------------------------- |
| **Frontend**      | React 19, Vite, React Router, Axios, Lucide Icons |
| **Backend**       | Python, FastAPI, Uvicorn, SQLAlchemy              |
| **AI/ML**         | Groq Llama-3 8B, HuggingFace all-MiniLM-L6-v2     |
| **Vector DB**     | Pinecone (Serverless)                             |
| **Database**      | SQLite (Production) / SQLite In-Memory (Tests)    |
| **Auth**          | JWT (python-jose), bcrypt (passlib)               |
| **RAG Framework** | LangChain                                         |
| **Testing**       | Pytest, HTTPX                                     |

---

<div align="center">

**Built with ❤️ using RAG Architecture**

_Upload. Ask. Discover._

</div>
