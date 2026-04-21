from threading import Lock
from typing import Dict, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent.graph import process_message


def _new_agent_state() -> Dict:
    return {
        "messages": [],
        "intent": "",
        "name": "",
        "email": "",
        "platform": "",
        "lead_captured": False,
        "lead_stage": "",
    }


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="User message")
    session_id: Optional[str] = None


class ResetRequest(BaseModel):
    session_id: str


app = FastAPI(title="AutoStream Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_sessions: Dict[str, Dict] = {}
_sessions_lock = Lock()


@app.get("/api/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat")
def chat(payload: ChatRequest) -> Dict:
    user_message = payload.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message must not be empty")

    session_id = payload.session_id or str(uuid4())

    with _sessions_lock:
        state = _sessions.setdefault(session_id, _new_agent_state())
        response = process_message(state, user_message)

        state_summary = {
            "intent": state.get("intent", ""),
            "name": state.get("name", ""),
            "email": state.get("email", ""),
            "platform": state.get("platform", ""),
            "lead_stage": state.get("lead_stage", ""),
            "lead_captured": state.get("lead_captured", False),
        }

    return {
        "session_id": session_id,
        "response": response,
        "state": state_summary,
    }


@app.post("/api/reset")
def reset(payload: ResetRequest) -> Dict[str, str]:
    with _sessions_lock:
        _sessions[payload.session_id] = _new_agent_state()
    return {"status": "reset"}
