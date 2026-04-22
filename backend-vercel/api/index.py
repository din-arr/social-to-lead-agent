from __future__ import annotations

import json
import os
import re
from pathlib import Path
from threading import Lock
from typing import Dict, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    from google import genai
except Exception:  # pragma: no cover
    genai = None


def load_knowledge_base() -> Dict:
    kb_path = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"
    with kb_path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


KB = load_knowledge_base()


def classify_intent(user_message: str) -> str:
    text = user_message.lower().strip()

    high_intent_keywords = [
        "sign up",
        "get started",
        "i want to try",
        "i want pro",
        "subscribe",
        "buy",
        "interested",
        "want to use",
        "want to join",
        "start pro",
        "try pro",
        "i want the pro plan",
        "start",
    ]

    inquiry_keywords = [
        "price",
        "pricing",
        "plan",
        "plans",
        "feature",
        "features",
        "refund",
        "support",
        "cost",
        "resolution",
        "videos",
    ]

    greeting_keywords = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening",
        "good afternoon",
    ]

    if any(phrase in text for phrase in high_intent_keywords):
        return "high_intent_lead"
    if any(phrase in text for phrase in inquiry_keywords):
        return "product_inquiry"
    if any(phrase in text for phrase in greeting_keywords):
        return "greeting"

    return "product_inquiry"


def detect_platform(text: str) -> str:
    text = text.lower().strip()
    platforms = {
        "youtube": "YouTube",
        "yt": "YouTube",
        "instagram": "Instagram",
        "insta": "Instagram",
        "ig": "Instagram",
        "tiktok": "TikTok",
        "tik tok": "TikTok",
        "linkedin": "LinkedIn",
        "facebook": "Facebook",
        "fb": "Facebook",
    }
    for key, value in platforms.items():
        if key in text:
            return value
    return ""


def is_valid_email(email: str) -> bool:
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email.strip()) is not None


def mock_lead_capture(name: str, email: str, platform: str) -> Dict[str, str]:
    return {
        "status": "success",
        "message": (
            f"Thanks {name}! Your interest for {platform} has been recorded. "
            f"Our team will contact you at {email} soon."
        ),
    }


def retrieve_answer(user_message: str) -> str:
    text = user_message.lower()
    plans = {p["name"].lower(): p for p in KB.get("plans", [])}
    basic = plans.get("basic")
    pro = plans.get("pro")

    if "price" in text or "pricing" in text:
        if basic and pro:
            return (
                f"AutoStream has two plans:\n"
                f"- Basic: {basic['price']} ({basic['videos_per_month']}, {basic['resolution']})\n"
                f"- Pro: {pro['price']} ({pro['videos_per_month']}, {pro['resolution']})"
            )
    if "feature" in text or "features" in text:
        basic_features = ", ".join(basic.get("features", [])) if basic else "none listed"
        pro_features = ", ".join(pro.get("features", [])) if pro else "none listed"
        return f"Basic features: {basic_features}. Pro features: {pro_features}."
    if "refund" in text:
        policies = KB.get("policies", [])
        refund_lines = [p for p in policies if "refund" in p.lower()]
        if refund_lines:
            return refund_lines[0]
        return "No refunds are available after 7 days."
    if "support" in text:
        return "24/7 support is available on the Pro plan."
    if "basic" in text and "pro" in text and basic and pro:
        return (
            f"Basic costs {basic['price']} with {basic['videos_per_month']} at {basic['resolution']}. "
            f"Pro costs {pro['price']} with {pro['videos_per_month']} at {pro['resolution']}."
        )
    if "basic" in text and basic:
        return (
            f"Basic plan: {basic['price']}, {basic['videos_per_month']}, "
            f"{basic['resolution']}."
        )
    if "pro" in text and pro:
        return (
            f"Pro plan: {pro['price']}, {pro['videos_per_month']}, "
            f"{pro['resolution']}."
        )
    return "Sorry, that detail is not available in the current knowledge base."


def retrieve_answer_with_llm(user_message: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key or genai is None:
        return retrieve_answer(user_message)

    context_lines = []
    for plan in KB.get("plans", []):
        context_lines.append(
            f"{plan.get('name')}: price={plan.get('price')}, "
            f"videos={plan.get('videos_per_month')}, "
            f"resolution={plan.get('resolution')}, "
            f"features={', '.join(plan.get('features', [])) or 'none'}"
        )
    for policy in KB.get("policies", []):
        context_lines.append(f"policy={policy}")

    prompt = (
        "You are an AI sales assistant for AutoStream.\n"
        "Answer using ONLY this context. If unavailable, reply exactly:\n"
        "Sorry, that detail is not available in the current knowledge base.\n\n"
        f"Context:\n{chr(10).join(context_lines)}\n\n"
        f"User question:\n{user_message}\n"
    )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )
        if hasattr(response, "text") and response.text:
            return response.text.strip()
    except Exception:
        pass

    return retrieve_answer(user_message)


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


@app.get("/")
def root() -> Dict[str, str]:
    return {"status": "ok", "service": "autostream-backend"}


@app.get("/api/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


def process_message(state: Dict, user_message: str) -> str:
    normalized_message = user_message.strip()
    intent = classify_intent(normalized_message)
    state["messages"].append({"role": "user", "content": normalized_message})
    state["intent"] = intent

    if state.get("lead_captured"):
        if intent == "product_inquiry":
            return retrieve_answer(normalized_message)
        return (
            "Your lead has already been captured successfully. "
            "You can still ask about pricing, features, or refunds."
        )

    lead_stage = state.get("lead_stage", "")
    if lead_stage == "awaiting_name":
        name = normalized_message.strip()
        if not name:
            return "Please share your name so I can continue the signup process."
        state["name"] = name
        state["lead_stage"] = "awaiting_email"
        return "Thanks! Please share your email address."

    if lead_stage == "awaiting_email":
        email = normalized_message.strip().lower()
        if not is_valid_email(email):
            return "Please share a valid email address."
        state["email"] = email
        if state.get("platform"):
            result = mock_lead_capture(state["name"], email, state["platform"])
            state["lead_captured"] = True
            state["lead_stage"] = "completed"
            return result["message"]
        state["lead_stage"] = "awaiting_platform"
        return (
            "Thanks! Which creator platform do you use? "
            "(YouTube, Instagram, TikTok, LinkedIn, Facebook)"
        )

    if lead_stage == "awaiting_platform":
        platform = detect_platform(normalized_message) or normalized_message.title()
        state["platform"] = platform
        result = mock_lead_capture(state.get("name", ""), state.get("email", ""), platform)
        state["lead_captured"] = True
        state["lead_stage"] = "completed"
        return result["message"]

    if intent == "greeting":
        return "Hi! I can help with AutoStream pricing, features, refunds, and sign-up."

    if intent == "product_inquiry":
        return retrieve_answer_with_llm(normalized_message)

    if intent == "high_intent_lead":
        state["lead_stage"] = "awaiting_name"
        detected_platform = detect_platform(normalized_message)
        if detected_platform:
            state["platform"] = detected_platform
        return "Great! You're interested in AutoStream. May I have your name?"

    return (
        "Sorry, I didn’t fully understand that. You can ask about pricing, "
        "features, refunds, or say 'start' to begin signup."
    )


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

    return {"session_id": session_id, "response": response, "state": state_summary}


@app.post("/api/reset")
def reset(payload: ResetRequest) -> Dict[str, str]:
    with _sessions_lock:
        _sessions[payload.session_id] = _new_agent_state()
    return {"status": "reset"}
