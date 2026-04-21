import re
from agent.intent import classify_intent
from agent.rag import retrieve_answer
from agent.tools import mock_lead_capture


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


def process_message(state, user_message: str) -> str:
    user_message = user_message.strip()
    state["messages"].append({"role": "user", "content": user_message})

    if "lead_stage" not in state:
        state["lead_stage"] = ""

    text = user_message.lower().strip()
    intent = classify_intent(user_message)

    if any(trigger in text for trigger in ["start", "get started", "signup", "sign up", "register", "join now"]):
        intent = "high_intent_lead"

    state["intent"] = intent

    if state.get("lead_captured", False):
        if intent == "product_inquiry":
            return retrieve_answer(user_message)

        return "Your lead has already been captured successfully. You can still ask about pricing, features, or refunds."

    if not state.get("platform"):
        detected_platform = detect_platform(user_message)
        if detected_platform:
            state["platform"] = detected_platform

    if intent == "greeting" and state.get("lead_stage") == "":
        return "Hi! I can help you with AutoStream pricing, features, refunds, and sign-up."

    if intent == "product_inquiry" and state.get("lead_stage") == "":
        return retrieve_answer(user_message)

    if intent == "high_intent_lead" and state.get("lead_stage") == "":
        state["lead_stage"] = "awaiting_name"
        return "Great! You're interested in AutoStream. May I have your name?"

    if state.get("lead_stage") == "awaiting_name":
        state["name"] = user_message
        state["lead_stage"] = "awaiting_email"
        return "Thanks! Please share your email address."

    if state.get("lead_stage") == "awaiting_email":
        if not is_valid_email(user_message):
            return "Please share a valid email address."

        state["email"] = user_message.lower()

        if state.get("platform"):
            result = mock_lead_capture(
                state["name"],
                state["email"],
                state["platform"]
            )
            state["lead_captured"] = True
            state["lead_stage"] = "completed"
            return result["message"]

        state["lead_stage"] = "awaiting_platform"
        return "Thanks! Which creator platform do you use? (YouTube, Instagram, TikTok, LinkedIn, Facebook)"

    if state.get("lead_stage") == "awaiting_platform":
        detected_platform = detect_platform(user_message)
        if detected_platform:
            state["platform"] = detected_platform
        else:
            state["platform"] = user_message.title()

        result = mock_lead_capture(
            state["name"],
            state["email"],
            state["platform"]
        )
        state["lead_captured"] = True
        state["lead_stage"] = "completed"
        return result["message"]

    if intent == "product_inquiry" and state.get("lead_stage") != "":
        answer = retrieve_answer(user_message)

        if state.get("lead_stage") == "awaiting_name":
            return answer + "\n\nWhen you're ready, please share your name."

        if state.get("lead_stage") == "awaiting_email":
            return answer + "\n\nWhen you're ready, please share your email address."

        if state.get("lead_stage") == "awaiting_platform":
            return answer + "\n\nWhen you're ready, please tell me your main creator platform."

    return "Sorry, I didn’t fully understand that. You can ask about pricing, features, refunds, or say 'start' to begin signup."