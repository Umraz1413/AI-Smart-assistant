# AI Smart Assistant

A productivity assistant that wraps Google's Gemini API in five focused tools: summarize, ask questions of a document, generate content, analyze text, and get prioritized action suggestions. FastAPI backend, React (Vite) frontend, Google Gemini API (**free tier, no credit card required**).

![status](https://img.shields.io/badge/status-active-brightgreen) ![license](https://img.shields.io/badge/license-MIT-blue)

## Why this exists

Most "AI assistant" demos are a single chat box. In real work, the same underlying model gets used for a handful of distinct jobs — condense this, answer this from that document, draft this email, tell me what to do next. This project treats each of those as its own module with its own prompt, its own input shape, and its own UI, instead of forcing everything through one generic textbox.

## Features

| Module | What it does |
|---|---|
| **Summarize** | Condenses text to short / medium / detailed length |
| **Ask** | Answers a question strictly from provided context (won't guess beyond it) |
| **Generate** | Drafts emails, blog posts, social posts, or outlines in a given tone |
| **Analyze** | Structured breakdown: overview, key points, tone, entities, gaps |
| **Suggest** | Turns a task list or brain-dump into a prioritized action plan |

## Architecture

```
ai-smart-assistant/
├── backend/                 FastAPI app
│   ├── main.py               App entrypoint, CORS, global error handlers
│   ├── config.py              Env-based settings (reads ANTHROPIC_API_KEY etc.)
│   ├── routes/                One router per feature (summarize, qa, generate, analyze, suggest)
│   ├── services/
│   │   └── claude_client.py   Single place that talks to the Anthropic API
│   ├── models/
│   │   └── schemas.py         Pydantic request/response models
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                 React + Vite app
│   ├── src/
│   │   ├── App.jsx             Module switcher / shell
│   │   ├── api/client.js       Fetch wrapper, typed errors, health check
│   │   └── components/         One component per module + shared ResultPanel/StatusBadge
│   ├── package.json
│   └── .env.example
│
├── .gitignore
├── LICENSE
└── README.md
```

**Why it's structured this way:** every route funnels through `services/claude_client.py`, so the API key is read from the environment in exactly one place, and error handling (rate limits, auth failures, network issues, empty responses) is written once instead of copy-pasted into five route files. The frontend mirrors that: one `api/client.js` module owns all backend communication, and each feature is an isolated component that manages its own loading/error/result state.

## Prerequisites

- Python 3.10+
- Node.js 18+
- A **free** [Google Gemini API key](https://aistudio.google.com/apikey) — no credit card required

## Setup

### 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# open .env and set GEMINI_API_KEY=... (get a free key at https://aistudio.google.com/apikey)

uvicorn main:app --reload
```

The API is now running at `http://localhost:8000`. Interactive docs (Swagger UI) are at `http://localhost:8000/docs`.

### 2. Frontend

In a second terminal:

```bash
cd frontend
npm install

cp .env.example .env   # only needed if your backend isn't on localhost:8000

npm run dev
```

Open `http://localhost:5173`. The header shows a live backend status badge — it will tell you directly if the server is unreachable or the API key isn't configured, instead of failing silently on the first request.

## API key handling

- The key lives only in `backend/.env`, which is git-ignored (`backend/.gitignore` entry + root `.gitignore`).
- `backend/config.py` reads it via `os.getenv` — it is never hardcoded, logged, or sent to the frontend.
- The frontend never touches the key at all; it only talks to your own backend, which then talks to Google.
- `.env.example` files are committed as templates so the repo is safe to push publicly.

## Why Gemini instead of a paid API

Google AI Studio's Flash models (`gemini-2.5-flash` by default here) are free with no credit card and no expiration — only rate limits (usually a low number of requests per minute and a daily cap, viewable in your AI Studio dashboard). That makes this project runnable end-to-end at zero cost. If you outgrow the free tier, `services/ai_client.py` is the only file that talks to the AI provider — swapping in a paid key, a different Gemini model, or a different provider entirely means editing one file.

## API reference

All endpoints are `POST` (except health) and return `{ "result": "...", "model": "...", "input_tokens": n, "output_tokens": n }` on success, or `{ "error": "..." }` with a non-2xx status on failure.

| Endpoint | Body |
|---|---|
| `GET /api/health` | — |
| `POST /api/summarize` | `{ "text": string, "length": "short"\|"medium"\|"detailed" }` |
| `POST /api/qa` | `{ "context": string, "question": string }` |
| `POST /api/generate` | `{ "prompt": string, "content_type": string, "tone": string }` |
| `POST /api/analyze` | `{ "text": string }` |
| `POST /api/suggest` | `{ "context": string }` |

Full schemas and a try-it-out console are available at `/docs` once the backend is running.

## Error handling & resilience

- **Backend:** `services/ai_client.py` catches Gemini SDK errors specifically (rate limits, auth/permission errors, server-side outages) and maps each to an appropriate HTTP status and a plain-language message, plus a catch-all for anything unexpected. Global FastAPI exception handlers in `main.py` guarantee every error, including validation errors, returns clean JSON rather than a stack trace.
- **Frontend:** `api/client.js` distinguishes network failures ("can't reach the backend") from backend errors (surfaced from the response body) via a typed `ApiError`. Every module shows a loading state while a request is in flight and a readable error state if it fails — nothing hangs or fails silently.
- **Input limits:** requests over `MAX_INPUT_CHARS` (default 20,000, configurable in `.env`) are rejected with a clear `413` before ever reaching the Anthropic API.

## Deploying

- **Backend:** any host that runs an ASGI app (Render, Fly.io, Railway, a VM behind `uvicorn`/`gunicorn`). Set `GEMINI_API_KEY` and `ALLOWED_ORIGINS` (your deployed frontend's origin) as environment variables on the host — do not bake them into the image.
- **Frontend:** `npm run build` produces a static `dist/` folder deployable to Vercel, Netlify, Cloudflare Pages, or any static host. Set `VITE_API_BASE_URL` to your deployed backend's URL at build time.

## Pushing to GitHub

```bash
cd ai-smart-assistant
git init
git add .
git commit -m "Initial commit: AI Smart Assistant"
git branch -M main
git remote add origin https://github.com/<your-username>/ai-smart-assistant.git
git push -u origin main
```

`.env` files are already excluded by `.gitignore`, so your API key won't be committed.

## Tech stack

- **Backend:** Python, FastAPI, Pydantic, google-genai SDK, Uvicorn
- **Frontend:** React 18, Vite
- **AI:** Google Gemini (free tier via Google AI Studio)

## License

MIT — see [LICENSE](LICENSE).
