import re

from langgraph.graph import END, START, StateGraph

from agent.intent import classify_intent
from agent.rag import retrieve_answer
from agent.state import AgentState
from agent.tools import mock_lead_capture

LEAD_TRIGGER_KEYWORDS = (
    "start",
    "get started",
    "signup",
    "sign up",
    "register",
    "join now",
)

PRODUCT_QUERY_KEYWORDS = (
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
)


def is_valid_email(email: str) -> bool:
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email.strip()) is not None


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


def is_product_question(text: str) -> bool:
    lower_text = text.lower()
    return "?" in lower_text or any(keyword in lower_text for keyword in PRODUCT_QUERY_KEYWORDS)


def classify_user_turn(state: AgentState) -> AgentState:
    user_message = state.get("user_message", "").strip()
    text = user_message.lower()

    messages = list(state.get("messages", []))
    messages.append({"role": "user", "content": user_message})

    intent = classify_intent(user_message)
    if any(trigger in text for trigger in LEAD_TRIGGER_KEYWORDS):
        intent = "high_intent_lead"

    updates: AgentState = {
        "messages": messages,
        "intent": intent,
    }

    if not state.get("platform"):
        detected_platform = detect_platform(user_message)
        if detected_platform:
            updates["platform"] = detected_platform

    return updates


def route_turn(state: AgentState) -> str:
    lead_stage = state.get("lead_stage", "")
    intent = state.get("intent", "")
    user_message = state.get("user_message", "").strip()

    if state.get("lead_captured", False):
        if intent == "product_inquiry":
            return "answer_product_query"
        return "lead_already_captured"

    if lead_stage == "awaiting_name":
        if intent == "product_inquiry" and is_product_question(user_message):
            return "answer_during_lead_capture"
        return "collect_name"

    if lead_stage == "awaiting_email":
        if is_valid_email(user_message):
            return "collect_email"
        if intent == "product_inquiry" and is_product_question(user_message):
            return "answer_during_lead_capture"
        return "collect_email"

    if lead_stage == "awaiting_platform":
        if intent == "product_inquiry" and is_product_question(user_message):
            return "answer_during_lead_capture"
        return "collect_platform"

    if intent == "greeting":
        return "handle_greeting"

    if intent == "product_inquiry":
        return "answer_product_query"

    if intent == "high_intent_lead":
        return "start_lead_capture"

    return "handle_fallback"


def handle_greeting(_: AgentState) -> AgentState:
    return {
        "response": "Hi! I can help you with AutoStream pricing, features, refunds, and sign-up."
    }


def answer_product_query(state: AgentState) -> AgentState:
    return {"response": retrieve_answer(state.get("user_message", ""))}


def answer_during_lead_capture(state: AgentState) -> AgentState:
    answer = retrieve_answer(state.get("user_message", ""))
    lead_stage = state.get("lead_stage", "")

    follow_up = ""
    if lead_stage == "awaiting_name":
        follow_up = "When you're ready, please share your name."
    elif lead_stage == "awaiting_email":
        follow_up = "When you're ready, please share your email address."
    elif lead_stage == "awaiting_platform":
        follow_up = "When you're ready, please share your creator platform."

    if follow_up:
        answer = f"{answer}\n\n{follow_up}"

    return {"response": answer}


def start_lead_capture(_: AgentState) -> AgentState:
    return {
        "lead_stage": "awaiting_name",
        "response": "Great! You're interested in AutoStream. May I have your name?",
    }


def collect_name(state: AgentState) -> AgentState:
    name = state.get("user_message", "").strip()
    if not name:
        return {"response": "Please share your name so I can continue the signup process."}

    return {
        "name": name,
        "lead_stage": "awaiting_email",
        "response": "Thanks! Please share your email address.",
    }


def collect_email(state: AgentState) -> AgentState:
    email = state.get("user_message", "").strip().lower()
    if not is_valid_email(email):
        return {"response": "Please share a valid email address."}

    updates: AgentState = {"email": email}

    if state.get("name") and state.get("platform"):
        result = mock_lead_capture(state["name"], email, state["platform"])
        updates.update(
            {
                "lead_captured": True,
                "lead_stage": "completed",
                "response": result["message"],
            }
        )
        return updates

    updates.update(
        {
            "lead_stage": "awaiting_platform",
            "response": "Thanks! Which creator platform do you use? (YouTube, Instagram, TikTok, LinkedIn, Facebook)",
        }
    )
    return updates


def collect_platform(state: AgentState) -> AgentState:
    user_text = state.get("user_message", "").strip()
    if not user_text:
        return {
            "response": "Please share your creator platform. For example: YouTube, Instagram, TikTok, LinkedIn, or Facebook."
        }

    platform = detect_platform(user_text) or user_text.title()

    result = mock_lead_capture(
        state.get("name", ""),
        state.get("email", ""),
        platform,
    )

    return {
        "platform": platform,
        "lead_captured": True,
        "lead_stage": "completed",
        "response": result["message"],
    }


def lead_already_captured(_: AgentState) -> AgentState:
    return {
        "response": "Your lead has already been captured successfully. You can still ask about pricing, features, or refunds."
    }


def handle_fallback(_: AgentState) -> AgentState:
    return {
        "response": "Sorry, I didn\'t fully understand that. You can ask about pricing, features, refunds, or say 'start' to begin signup."
    }


def _build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("classify_user_turn", classify_user_turn)
    workflow.add_node("handle_greeting", handle_greeting)
    workflow.add_node("answer_product_query", answer_product_query)
    workflow.add_node("answer_during_lead_capture", answer_during_lead_capture)
    workflow.add_node("start_lead_capture", start_lead_capture)
    workflow.add_node("collect_name", collect_name)
    workflow.add_node("collect_email", collect_email)
    workflow.add_node("collect_platform", collect_platform)
    workflow.add_node("lead_already_captured", lead_already_captured)
    workflow.add_node("handle_fallback", handle_fallback)

    workflow.add_edge(START, "classify_user_turn")

    workflow.add_conditional_edges(
        "classify_user_turn",
        route_turn,
        {
            "handle_greeting": "handle_greeting",
            "answer_product_query": "answer_product_query",
            "answer_during_lead_capture": "answer_during_lead_capture",
            "start_lead_capture": "start_lead_capture",
            "collect_name": "collect_name",
            "collect_email": "collect_email",
            "collect_platform": "collect_platform",
            "lead_already_captured": "lead_already_captured",
            "handle_fallback": "handle_fallback",
        },
    )

    for node_name in [
        "handle_greeting",
        "answer_product_query",
        "answer_during_lead_capture",
        "start_lead_capture",
        "collect_name",
        "collect_email",
        "collect_platform",
        "lead_already_captured",
        "handle_fallback",
    ]:
        workflow.add_edge(node_name, END)

    return workflow.compile()


AGENT_GRAPH = _build_graph()


def process_message(state: dict, user_message: str) -> str:
    normalized_message = user_message.strip()

    state.setdefault("messages", [])
    state.setdefault("intent", "")
    state.setdefault("name", "")
    state.setdefault("email", "")
    state.setdefault("platform", "")
    state.setdefault("lead_captured", False)
    state.setdefault("lead_stage", "")

    result = AGENT_GRAPH.invoke(
        {
            **state,
            "user_message": normalized_message,
        }
    )

    persistent_keys = [
        "messages",
        "intent",
        "name",
        "email",
        "platform",
        "lead_captured",
        "lead_stage",
    ]
    for key in persistent_keys:
        if key in result:
            state[key] = result[key]

    return result.get("response", "Sorry, I couldn't generate a response.")
