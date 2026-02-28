# Frontend Guide

The RAG Bot interface is built with React 19 and Vite. It heavily relies on modern hooks and standard `react-router-dom` for client-side routing.

## Technology Stack

- **React (`^19.2.0`)**: Modern functional components and hooks (`useState`, `useEffect`).
- **Vite**: Extremely fast bundler and dev server.
- **React Router DOM (`^7.13.1`)**: SPA routing logic (`Routes`, `Route`, `Navigate`).
- **Axios (`^1.13.6`)**: Handling HTTP requests to the FastAPI backend.
- **Lucide-React (`^0.575.0`)**: Lightweight SVG icons for the UI.
- **React Markdown & Remark GFM**: Rendering markdown responses from the LLM cleanly in the chat interface.

## Project Structure

```text
frontend/
├── package.json
├── index.html
├── vite.config.js
└── src/
    ├── main.jsx          # Entry point, registers standard CSS
    ├── index.css         # Global tailwind-like styles & Tailwind configuration
    ├── App.jsx           # Main routing layer, Auth context logic
    └── components/
        ├── Login.jsx     # Registration & Login logic
        ├── Upload.jsx    # File drag-and-drop or selection input for Document Ingestion
        └── Chat.jsx      # The primary conversation UI mimicking modern AI chat layouts
```

## Key Components

### 1. App.jsx (Routing & Layout)

The `App.jsx` handles core logic such as:

- Checking `localStorage` for the active `token`.
- Providing a generic side-navbar for navigation between Dashboard tasks (Chat, Documents).
- Guarding protected routes, ensuring unauthenticated users act exclusively inside `/login`.

### 2. Login.jsx

Provides a clean, two-pane layout to toggle between **Sign In** and **Sign Up**. It interacts directly with `/auth/login` and `/auth/register` on the backend, subsequently storing the JWT token on success.

### 3. Upload.jsx

Fetches the current user’s uploaded files via `GET /documents`. It includes an interactive drop zone wrapper that submits raw multiparts via `POST /documents/upload`, then triggers an immediate refresh of the document list.

### 4. Chat.jsx

The stateful conversation view.

- Maintains a `messages` array representing the chat history.
- Shows a loading spinner (`isThinking`) whilst the backend vectorizes the prompt and queries the AI.
- Renders AI outputs utilizing `react-markdown` to ensure lists and code blocks appear structured.
- Displays a list of `Sources` below AI responses to guarantee data provenance.
