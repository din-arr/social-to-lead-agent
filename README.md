# AutoStream Social-to-Lead Agent

This project now uses your **grand-entrance-3d UI/UX** (including GLB 3D models) and keeps the same assignment backend logic (LangGraph + RAG + gated lead tool execution).

## What Is Included
- `frontend/`: exact 3D React/TanStack UI adapted for AutoStream
- `agent/`: existing backend logic (intent, RAG, lead flow)
- `backend_api.py`: API wrapper that connects frontend to `process_message()`
- `data/knowledge_base.json`: local pricing/policies knowledge base

## Architecture
- **Frontend:** React + TanStack Router + Three.js (`helmet.glb`, `robot.glb`)
- **Backend Logic:** LangGraph flow in `agent/graph.py`
- **API Layer:** FastAPI (`/api/chat`, `/api/reset`, `/api/health`)
- **State:** server-side session state keyed by `session_id`

## Run Locally

### 1) Python backend
```bash
cd /Users/parthbandwal/Desktop/p/social-to-lead-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend_api:app --host 0.0.0.0 --port 8010 --reload
```

### 2) Frontend (new terminal)
```bash
cd /Users/parthbandwal/Desktop/p/social-to-lead-agent/frontend
npm install
cp .env.example .env
npm run dev
```

Open the frontend URL shown by Vite (usually `http://127.0.0.1:5173`).

## API Endpoints
- `GET /api/health`
- `POST /api/chat`
  - request: `{ "message": "...", "session_id": "optional" }`
  - response: `{ "session_id", "response", "state" }`
- `POST /api/reset`
  - request: `{ "session_id": "..." }`

## Assignment Requirements Mapping
- Intent classification: `agent/intent.py`
- RAG from local KB: `agent/rag.py` + `data/knowledge_base.json`
- Stateful memory across turns: LangGraph state + API session store
- Tool execution only after full qualification: `agent/graph.py` + `agent/tools.py`

## Notes
- `mock_lead_capture()` still prints the required line:
  `Lead captured successfully: <name>, <email>, <platform>`
- If `GOOGLE_API_KEY` is missing, deterministic fallback answers still work.
