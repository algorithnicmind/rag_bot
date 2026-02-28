<div align="center">
  <h1 align="center">RAG Bot - Internal Docs Q&A Agent</h1>

  <p align="center">
    A full-stack AI-powered application for securely chatting with your documents!
    <br />
    <a href="#features"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#getting-started">Getting Started</a>
    ·
    <a href="#api-endpoints">API Endpoints</a>
    ·
    <a href="#built-with">Tech Stack</a>
  </p>
</div>

<br />

> [!NOTE]
> This project implements a Retrieval-Augmented Generation (RAG) architecture to provide accurate, context-aware answers to user queries based on uploaded documents.

## 🚀 About The Project

**RAG Bot** allows users to securely upload documents (PDF, DOCX, TXT) and interactively chat with them. By leveraging vector embeddings and a modern Chat UI, it provides precise answers extracted directly from your internal documents.

### ✨ Features

- **Authentication System**: Secure user registration and login with JWT access tokens.
- **Document Management**: Upload and manage your personal documents securely.
- **RAG Engine**: Extracts text from documents, generates vector embeddings, and stores them in a highly-optimized Vector Database (Pinecone).
- **Interactive Chat Interface**: Ask natural language questions and receive AI-generated answers with source tracking.
- **Modern UI**: A visually pleasing and responsive React interface.

### 🛠️ Built With

- [![React][React.js]][React-url]
- [![FastAPI][FastAPI]][FastAPI-url]
- [![Vite][Vite]][Vite-url]
- [![Python][Python]][Python-url]

---

## 🚦 Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

Ensure you have the following installed on your machine:

- **Node.js** (v18+)
- **Python** (3.9+)

### Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/your_username/rag_bot.git
   cd rag_bot
   ```

<details>
<summary><strong>2. 🐍 Backend Setup (FastAPI)</strong></summary>
<br />

Navigate to the backend directory and set up the Python environment:

```sh
cd backend
python -m venv venv
```

**Activate the virtual environment:**

- On Windows:
  ```sh
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```sh
  source venv/bin/activate
  ```

**Install dependencies:**

```sh
pip install -r requirements.txt
```

> [!IMPORTANT]
> You must create a `.env` file in the `backend` directory.

Add your environment variables to the `.env` file:

```ini
PINECONE_API_KEY=your_pinecone_api_key
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_jwt_secret_key
```

**Run the FastAPI server:**

```sh
uvicorn main:app --reload
```

</details>

<details>
<summary><strong>3. ⚛️ Frontend Setup (React/Vite)</strong></summary>
<br />

Open a new terminal, navigate to the frontend directory:

```sh
cd frontend
npm install
npm run dev
```

> [!TIP]
> The frontend application will run on `http://localhost:5173` by default.

</details>

---

## 📡 API Endpoints

The FastAPI backend exposes the following key endpoints:

| Method | Endpoint            | Description                                                   |
| ------ | ------------------- | ------------------------------------------------------------- |
| `POST` | `/auth/register`    | Register a new user                                           |
| `POST` | `/auth/login`       | Login to retrieve JWT Access Token                            |
| `GET`  | `/users/me`         | Fetch detailed info of logged-in user                         |
| `POST` | `/documents/upload` | Upload and vectorize a new document (`.pdf`, `.docx`, `.txt`) |
| `GET`  | `/documents`        | Retrieve all documents uploaded by the user                   |
| `POST` | `/chat`             | Chat with the RAG engine based on uploaded documents          |

> [!TIP]
> Once the backend server is running, visit `http://127.0.0.1:8000/docs` to view the interactive **Swagger UI** for testing API endpoints.

---

## 🔒 Security

> [!CAUTION]
> Never commit your `.env` file containing API keys to GitHub. Ensure `.env` is listed in your `.gitignore`.

This project implements robust token-based authentication to ensure users can only query information from documents they have personally uploaded.

---

<div align="center">
  <p>Built with ❤️</p>
</div>

<!-- Markdowns & Links -->

[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[Vite]: https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white
[Vite-url]: https://vitejs.dev/
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
