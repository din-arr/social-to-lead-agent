# AutoStream Social-to-Lead Agent

Conversational AI agent for the ServiceHive Inflx assignment.

## Deliverables Included
- Agent logic with intent detection and LangGraph state flow
- RAG pipeline using local knowledge base (`data/knowledge_base.json`)
- Lead capture tool with strict gating (`name -> email -> platform`)
- `requirements.txt` with Python dependencies
- Frontend UI (3D experience) connected to backend chat API

## Project Structure
- `agent/intent.py`: intent classification (`greeting`, `product_inquiry`, `high_intent_lead`)
- `agent/rag.py`: retrieval + answer generation (with fallback)
- `agent/graph.py`: LangGraph workflow + state transitions
- `agent/tools.py`: `mock_lead_capture(name, email, platform)`
- `backend_api.py`: FastAPI bridge (`/api/chat`, `/api/reset`, `/api/health`)
- `data/knowledge_base.json`: pricing/features/policies knowledge
- `frontend/`: UI layer

## How To Run Locally
### 1) Backend
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

Open the URL shown by Vite (usually `http://127.0.0.1:5173`).

## Architecture Explanation (~200 words)
I chose **LangGraph** because this assignment needs deterministic, multi-turn control rather than a single prompt response. The workflow has explicit nodes for intent classification, product-question answering, lead capture stages, and fallback behavior. Using a graph makes it clear when each branch is allowed to run, which prevents premature tool calls and keeps the conversation stable across user intent shifts.

State is managed in a structured object (`messages`, `intent`, `lead_stage`, `name`, `email`, `platform`, `lead_captured`) and persists across turns through the backend session store. This satisfies the requirement to retain memory over 5-6 turns. RAG is implemented with a local JSON knowledge base, sentence-transformer embeddings, and a FAISS index. For each inquiry, relevant context is retrieved and used for response generation; if the model/API is unavailable, the system returns deterministic fallback answers so behavior stays reliable during demos.

Tool execution is isolated in `mock_lead_capture`, and the LangGraph flow only reaches that node after all required fields are present. This enforces the assignment rule that lead capture must not trigger before collecting **name**, **email**, and **creator platform**.

## WhatsApp Deployment (Webhook Integration)
To integrate this agent with WhatsApp, I would deploy a webhook API (FastAPI) behind HTTPS and connect it to either Meta WhatsApp Cloud API or Twilio WhatsApp.

Flow:
1. WhatsApp sends inbound message events to webhook endpoint.
2. Webhook maps sender phone number to a stored conversation session.
3. Backend calls `process_message(state, user_text)` and gets agent response.
4. Response is sent back to WhatsApp send-message API.
5. Updated session state is persisted for next message.

Production considerations:
- verify webhook signatures
- add retry/idempotency handling for duplicated events
- secure PII (name/email) in encrypted storage
- add logs/metrics for intent, tool calls, and failure paths

## API Endpoints
- `GET /api/health`
- `POST /api/chat` with `{ "message": "...", "session_id": "optional" }`
- `POST /api/reset` with `{ "session_id": "..." }`

## Note
`mock_lead_capture()` prints the required assignment output format:
`Lead captured successfully: <name>, <email>, <platform>`
